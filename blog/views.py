from __future__ import annotations

from functools import wraps

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .models import Post, Setting, db
from .utils import ensure_unique_slug


public_bp = Blueprint("public", __name__)
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login", next=request.path))
        return view_func(*args, **kwargs)

    return wrapped_view


@public_bp.get("/")
def home():
    posts = (
        Post.query.filter_by(is_published=True)
        .order_by(Post.created_at.desc())
        .all()
    )
    featured_post = posts[0] if posts else None
    recent_posts = posts[1:7] if len(posts) > 1 else []
    return render_template(
        "public/home.html",
        featured_post=featured_post,
        recent_posts=recent_posts,
        posts_count=len(posts),
    )


@public_bp.get("/post/<slug>")
def post_detail(slug: str):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template("public/post_detail.html", post=post)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if (
            username == current_app.config["ADMIN_USERNAME"]
            and password == current_app.config["ADMIN_PASSWORD"]
        ):
            session["is_admin"] = True
            flash("Вы вошли в админку.", "success")
            return redirect(request.args.get("next") or url_for("admin.dashboard"))
        flash("Неверный логин или пароль.", "error")
    return render_template("admin/login.html")


@admin_bp.post("/logout")
def logout():
    session.clear()
    flash("Сессия завершена.", "success")
    return redirect(url_for("public.home"))


@admin_bp.get("/")
@admin_required
def dashboard():
    posts = Post.query.order_by(Post.updated_at.desc()).all()
    return render_template("admin/dashboard.html", posts=posts)


@admin_bp.route("/posts/new", methods=["GET", "POST"])
@admin_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()
        cover_image = request.form.get("cover_image", "").strip() or None
        is_published = request.form.get("is_published") == "on"

        if not title or not excerpt or not content:
            flash("Заполните заголовок, описание и текст поста.", "error")
            return render_template("admin/post_form.html", post=None)

        post = Post(
            title=title,
            slug=ensure_unique_slug(title),
            excerpt=excerpt,
            content=content,
            cover_image=cover_image,
            is_published=is_published,
        )
        db.session.add(post)
        db.session.commit()
        flash("Пост создан.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/post_form.html", post=None)


@admin_bp.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        content = request.form.get("content", "").strip()
        cover_image = request.form.get("cover_image", "").strip() or None
        is_published = request.form.get("is_published") == "on"

        if not title or not excerpt or not content:
            flash("Заполните заголовок, описание и текст поста.", "error")
            return render_template("admin/post_form.html", post=post)

        post.title = title
        post.slug = ensure_unique_slug(title, current_post_id=post.id)
        post.excerpt = excerpt
        post.content = content
        post.cover_image = cover_image
        post.is_published = is_published

        db.session.commit()
        flash("Пост обновлен.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/post_form.html", post=post)


@admin_bp.post("/posts/<int:post_id>/delete")
@admin_required
def delete_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Пост удален.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    if request.method == "POST":
        keys = ("site_title", "site_tagline", "hero_title", "hero_text")
        for key in keys:
            value = request.form.get(key, "").strip()
            record = Setting.query.get(key)
            if record is None:
                record = Setting(key=key, value=value)
                db.session.add(record)
            else:
                record.value = value
        db.session.commit()
        flash("Настройки сохранены.", "success")
        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html")


@public_bp.app_errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404
