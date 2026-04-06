from __future__ import annotations

from typing import Any

from django.contrib.sitemaps import Sitemap

from django_growth.config import GrowthConfig, get_growth_config


class GrowthEmptySitemap(Sitemap):
    """Valid empty urlset when the host project has not registered any sitemaps."""

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return []


def get_sitemaps(config: GrowthConfig | None = None) -> dict[str, Any]:
    """
    Return the dict passed to Django's sitemap view.

    Uses ``config.sitemaps`` when non-empty; otherwise a single empty section
    named ``growth``.
    """
    if config is None:
        config = get_growth_config()
    registered = config.sitemaps
    if registered:
        return registered
    return {"growth": GrowthEmptySitemap}
