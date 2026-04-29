from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'blog.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
    SITE_TITLE = os.getenv("SITE_TITLE", "North Journal")
    SITE_TAGLINE = os.getenv("SITE_TAGLINE", "Minimal stories, clear interface.")
    HERO_TITLE = os.getenv("HERO_TITLE", "A clean publishing space")
    HERO_TEXT = os.getenv(
        "HERO_TEXT",
        "Write updates, essays and announcements without a bulky CMS.",
    )
