import re

from django.core.checks import Tags, Warning, register

from django_growth.config import get_growth_config
from django_growth.defaults import ENV_PRODUCTION

_VERIFICATION_RE = re.compile(r"^[A-Za-z0-9_-]{8,200}$")


@register(Tags.compatibility)
def growth_settings_check(app_configs, **kwargs):
    errors = []
    config = get_growth_config()

    if config.env == ENV_PRODUCTION and not config.gtm_id:
        errors.append(
            Warning(
                "GROWTH['ENV'] is 'production' but GROWTH['GTM_ID'] is empty; "
                "GTM snippets will not render.",
                id="django_growth.W001",
            )
        )

    if config.google_verification and not _VERIFICATION_RE.match(
        config.google_verification
    ):
        errors.append(
            Warning(
                "GROWTH['GOOGLE_VERIFICATION'] is set but does not look like a "
                "typical Search Console HTML-tag token.",
                id="django_growth.W002",
            )
        )

    return errors
