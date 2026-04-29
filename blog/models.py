from __future__ import annotations

from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.String(320), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(500), nullable=True)
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Setting(db.Model):
    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.Text, nullable=False)

    @classmethod
    def bootstrap_defaults(cls, config: dict) -> None:
        defaults = {
            "site_title": config["SITE_TITLE"],
            "site_tagline": config["SITE_TAGLINE"],
            "hero_title": config["HERO_TITLE"],
            "hero_text": config["HERO_TEXT"],
        }
        changed = False
        for key, value in defaults.items():
            if cls.query.get(key) is None:
                db.session.add(cls(key=key, value=value))
                changed = True
        if changed:
            db.session.commit()

    @classmethod
    def as_dict(cls) -> dict:
        data = {item.key: item.value for item in cls.query.all()}
        return {
            "site_title": data.get("site_title", current_app.config["SITE_TITLE"]),
            "site_tagline": data.get(
                "site_tagline", current_app.config["SITE_TAGLINE"]
            ),
            "hero_title": data.get("hero_title", current_app.config["HERO_TITLE"]),
            "hero_text": data.get("hero_text", current_app.config["HERO_TEXT"]),
        }
