from __future__ import annotations

from slugify import slugify

from .models import Post


def ensure_unique_slug(title: str, current_post_id: int | None = None) -> str:
    base_slug = slugify(title) or "post"
    slug = base_slug
    index = 2

    while True:
        query = Post.query.filter_by(slug=slug)
        if current_post_id is not None:
            query = query.filter(Post.id != current_post_id)
        if query.first() is None:
            return slug
        slug = f"{base_slug}-{index}"
        index += 1
