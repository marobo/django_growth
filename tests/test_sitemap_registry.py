from django.test import SimpleTestCase

from django_growth.config import growth_config_from_mapping
from django_growth.sitemap_registry import GrowthEmptySitemap, get_sitemaps


class SitemapRegistryTests(SimpleTestCase):
    def test_empty_registry_uses_placeholder(self):
        config = growth_config_from_mapping({}, debug=False)
        sitemaps = get_sitemaps(config)
        self.assertIn("growth", sitemaps)
        self.assertIs(sitemaps["growth"], GrowthEmptySitemap)

    def test_registered_sitemaps_passthrough(self):
        sentinel = object()
        config = growth_config_from_mapping({"SITEMAPS": {"blog": sentinel}}, debug=False)
        sitemaps = get_sitemaps(config)
        self.assertEqual(sitemaps["blog"], sentinel)
