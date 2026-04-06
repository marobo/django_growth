from __future__ import annotations

from django.urls import reverse

from django_growth.config import GrowthConfig


def build_robots_txt(
    config: GrowthConfig,
    request,
    *,
    sitemap_url_name: str = "django_growth:sitemap",
) -> str:
    """
    Build the ``robots.txt`` body (no HTTP wrapper).

    ``request`` is used for :meth:`~django.http.HttpRequest.build_absolute_uri`
    when emitting the ``Sitemap:`` line.
    """
    lines = ["User-agent: *"]
    if config.robots_disallow_all:
        lines.append("Disallow: /")
    else:
        lines.append("Allow: /")

    if config.robots_include_sitemap and not config.robots_disallow_all:
        sitemap_url = request.build_absolute_uri(reverse(sitemap_url_name))
        lines.append(f"Sitemap: {sitemap_url}")

    return "\n".join(lines) + "\n"
