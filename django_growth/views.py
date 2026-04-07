from django.http import HttpResponse
from django.views.generic import View

from django_growth.config import get_growth_config_for_request
from django_growth.robots import build_robots_txt


class RobotsTxtView(View):
    """
    Serve ``robots.txt`` with correct GET and HEAD handling.

    Some crawlers and SEO tools issue a HEAD request first; supporting HEAD
    avoids spurious "unable to verify robots.txt" failures.
    """

    http_method_names = ["get", "head"]

    def get(self, request):
        config = get_growth_config_for_request(request)
        body = build_robots_txt(config, request)
        response = HttpResponse(body, content_type="text/plain; charset=utf-8")
        response["Cache-Control"] = "public, max-age=3600"
        return response

    def head(self, request):
        response = self.get(request)
        nbytes = len(response.content)
        response.content = b""
        response["Content-Length"] = str(nbytes)
        return response
