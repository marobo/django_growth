"""
Default values and documented ``GROWTH`` keys for django_growth.

Host projects override via ``settings.GROWTH`` (dict). Unknown keys are ignored.
"""

# String defaults (empty = disabled / omitted where applicable)
DEFAULT_GTM_ID = ""
DEFAULT_SITE_NAME = ""
DEFAULT_GOOGLE_VERIFICATION = ""

# Inferred from ``settings.DEBUG`` when ENV is omitted or blank
ENV_DEVELOPMENT = "development"
ENV_PRODUCTION = "production"
