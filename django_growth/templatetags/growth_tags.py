from django import template

from django_growth.config import get_growth_config_for_request

register = template.Library()


def _blank_str(value):
    if value is None:
        return ""
    return str(value).strip()


def _config(context):
    request = context.get("request")
    return get_growth_config_for_request(request)


@register.inclusion_tag("django_growth/gtm.html", takes_context=True)
def growth_gtm(context):
    config = _config(context)
    return {
        "show_gtm": config.gtm_snippets_enabled,
        "gtm_id": config.gtm_id,
    }


@register.inclusion_tag("django_growth/gtm_body.html", takes_context=True)
def growth_gtm_body(context):
    config = _config(context)
    return {
        "show_gtm": config.gtm_snippets_enabled,
        "gtm_id": config.gtm_id,
    }


@register.inclusion_tag("django_growth/meta.html", takes_context=True)
def growth_meta(
    context,
    title=None,
    description="",
    og_image="",
    og_type="website",
    canonical_url=None,
    twitter_card="summary_large_image",
    robots=None,
    site_title_suffix=True,
):
    config = _config(context)
    site_name = config.site_name
    google_verification = config.google_verification

    title = "" if title is None else str(title).strip()
    description = _blank_str(description)
    og_image = _blank_str(og_image) or config.default_og_image
    og_type = _blank_str(og_type) or "website"
    twitter_card = _blank_str(twitter_card) or "summary_large_image"
    if not og_image and twitter_card == "summary_large_image":
        twitter_card = "summary"
    robots = None if robots is None else str(robots).strip()
    if robots == "":
        robots = None

    if site_title_suffix and site_name and title:
        page_title = f"{title} | {site_name}"
    elif title:
        page_title = title
    else:
        page_title = site_name

    og_title = page_title
    og_description = description

    request = context.get("request")
    if canonical_url is not None and str(canonical_url).strip() != "":
        page_url = str(canonical_url).strip()
    elif request is not None:
        page_url = request.build_absolute_uri()
    else:
        page_url = ""

    return {
        "page_title": page_title,
        "meta_description": description,
        "canonical_url": page_url,
        "og_title": og_title,
        "og_description": og_description,
        "og_image": og_image,
        "og_type": og_type,
        "og_url": page_url,
        "site_name": site_name,
        "twitter_card": twitter_card,
        "robots": robots,
        "google_verification": google_verification,
        "show_google_verification": bool(google_verification),
    }


@register.inclusion_tag("django_growth/includes/analytics.html")
def growth_analytics():
    return {}
