from django.contrib.sitemaps.views import sitemap
from django.urls import path

from django_growth import views
from django_growth.config import get_growth_config_for_request
from django_growth.sitemap_registry import get_sitemaps

app_name = "django_growth"


def growth_sitemap(request):
    config = get_growth_config_for_request(request)
    return sitemap(request, sitemaps=get_sitemaps(config))


urlpatterns = [
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", growth_sitemap, name="sitemap"),
]
