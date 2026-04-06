from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from django.conf import settings

from django_growth.defaults import (
    DEFAULT_GOOGLE_VERIFICATION,
    DEFAULT_GTM_ID,
    DEFAULT_SITE_NAME,
    ENV_DEVELOPMENT,
    ENV_PRODUCTION,
)


def _blank_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _as_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return bool(value)


@dataclass(frozen=True)
class GrowthConfig:
    """Resolved configuration from ``settings.GROWTH`` and ``settings.DEBUG``."""

    gtm_id: str
    site_name: str
    env: str
    google_verification: str
    sitemaps: dict[str, Any]
    robots_disallow_all: bool
    robots_include_sitemap: bool

    @property
    def gtm_snippets_enabled(self) -> bool:
        """GTM head/body snippets should render (production + non-empty container ID)."""
        return self.env == ENV_PRODUCTION and bool(self.gtm_id)

    def as_template_context(self) -> dict[str, str]:
        """Keys expected in templates as ``growth.*`` (uppercase for historical compatibility)."""
        return {
            "GTM_ID": self.gtm_id,
            "SITE_NAME": self.site_name,
            "ENV": self.env,
            "GOOGLE_VERIFICATION": self.google_verification,
        }


def _build_growth_config(raw: dict[str, Any], *, debug: bool) -> GrowthConfig:
    gtm_id = _blank_str(raw.get("GTM_ID", DEFAULT_GTM_ID))
    site_name = _blank_str(raw.get("SITE_NAME", DEFAULT_SITE_NAME))
    google_verification = _blank_str(
        raw.get("GOOGLE_VERIFICATION", DEFAULT_GOOGLE_VERIFICATION)
    )

    env_raw = raw.get("ENV", None)
    if env_raw is None or _blank_str(env_raw) == "":
        env = ENV_DEVELOPMENT if debug else ENV_PRODUCTION
    else:
        env = _blank_str(env_raw)

    sitemaps = raw.get("SITEMAPS")
    if not isinstance(sitemaps, dict):
        sitemaps = {}

    robots_disallow_all = _as_bool(raw.get("ROBOTS_DISALLOW_ALL"), default=debug)
    robots_include_sitemap = _as_bool(raw.get("ROBOTS_INCLUDE_SITEMAP"), default=True)

    return GrowthConfig(
        gtm_id=gtm_id,
        site_name=site_name,
        env=env,
        google_verification=google_verification,
        sitemaps=dict(sitemaps),
        robots_disallow_all=robots_disallow_all,
        robots_include_sitemap=robots_include_sitemap,
    )


def get_growth_config() -> GrowthConfig:
    """
    Read and normalize ``settings.GROWTH``.

    If ``GROWTH`` is missing or not a dict, it is treated as empty.
    """
    raw = getattr(settings, "GROWTH", None)
    if not isinstance(raw, dict):
        raw = {}
    return _build_growth_config(raw, debug=settings.DEBUG)


def get_growth_config_for_request(request=None) -> GrowthConfig:
    """
    Resolved config for the current request.

    Host projects can wrap this later for per-host overrides; the default
    implementation ignores ``request``.
    """
    return get_growth_config()


def growth_config_from_mapping(
    mapping: Mapping[str, Any], *, debug: bool = False
) -> GrowthConfig:
    """
    Build a :class:`GrowthConfig` from a mapping (e.g. unit tests).

    Uses the same normalization as :func:`get_growth_config`. When ``ENV`` is
    omitted or blank, ``debug`` drives the inferred environment (same as
    ``settings.DEBUG`` in :func:`get_growth_config`).
    """
    return _build_growth_config(dict(mapping), debug=debug)
