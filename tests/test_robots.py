from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import NoReverseMatch

from django_growth.config import growth_config_from_mapping
from django_growth.defaults import ENV_PRODUCTION
from django_growth.robots import build_robots_txt


class RobotsTxtTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_disallow_all_omits_sitemap(self):
        config = growth_config_from_mapping(
            {"ROBOTS_DISALLOW_ALL": True, "ROBOTS_INCLUDE_SITEMAP": True},
            debug=False,
        )
        request = self.factory.get("/robots.txt", HTTP_HOST="example.com")
        body = build_robots_txt(config, request)
        self.assertIn("Disallow: /", body)
        self.assertNotIn("Sitemap:", body)

    def test_allow_includes_sitemap_absolute_url(self):
        config = growth_config_from_mapping(
            {"ROBOTS_DISALLOW_ALL": False, "ROBOTS_INCLUDE_SITEMAP": True},
            debug=False,
        )
        request = self.factory.get("/robots.txt", HTTP_HOST="example.com", secure=True)
        body = build_robots_txt(config, request)
        self.assertIn("Allow: /", body)
        self.assertIn("Sitemap: https://example.com/sitemap.xml", body)

    @override_settings(GROWTH={"ROBOTS_INCLUDE_SITEMAP": False}, DEBUG=False)
    def test_include_sitemap_false(self):
        from django_growth.config import get_growth_config

        config = get_growth_config()
        request = self.factory.get("/robots.txt", HTTP_HOST="example.org")
        body = build_robots_txt(config, request)
        self.assertNotIn("Sitemap:", body)

    @patch("django_growth.robots.reverse", side_effect=NoReverseMatch())
    def test_sitemap_line_omitted_when_sitemap_url_missing(self, _mock_reverse):
        config = growth_config_from_mapping(
            {"ROBOTS_DISALLOW_ALL": False, "ROBOTS_INCLUDE_SITEMAP": True},
            debug=False,
        )
        request = self.factory.get("/robots.txt", HTTP_HOST="example.com")
        body = build_robots_txt(config, request)
        self.assertIn("Allow: /", body)
        self.assertNotIn("Sitemap:", body)
