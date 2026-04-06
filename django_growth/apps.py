from django.apps import AppConfig


class DjangoGrowthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_growth"
    label = "django_growth"
    verbose_name = "Django Growth"

    def ready(self):
        from django_growth import checks  # noqa: F401
