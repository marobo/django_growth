from django.http import HttpResponse

from django_growth.config import get_growth_config_for_request
from django_growth.robots import build_robots_txt


def robots_txt(request):
    config = get_growth_config_for_request(request)
    body = build_robots_txt(config, request)
    response = HttpResponse(body, content_type="text/plain; charset=utf-8")
    response["Cache-Control"] = "public, max-age=3600"
    return response
