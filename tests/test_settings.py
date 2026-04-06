SECRET_KEY = "test-key-not-for-production"
USE_TZ = True
DEBUG = True
ALLOWED_HOSTS = ["testserver", "localhost", "example.com"]
# Explicit dev-shaped GROWTH keeps system checks quiet during the suite.
GROWTH = {"ENV": "development"}
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django_growth",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
MIDDLEWARE = []
ROOT_URLCONF = "tests.urls_test"
SITE_ID = 1
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django_growth.context_processors.growth",
            ],
        },
    },
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
