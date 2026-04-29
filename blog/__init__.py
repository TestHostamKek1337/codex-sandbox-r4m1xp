from __future__ import annotations

from pathlib import Path

from flask import Flask

from config import Config
from .models import Post, Setting, db
from .views import admin_bp, public_bp


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        Setting.bootstrap_defaults(app.config)

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals() -> dict:
        settings = Setting.as_dict()
        return {
            "site_settings": settings,
            "draft_count": Post.query.filter_by(is_published=False).count(),
        }

    return app
