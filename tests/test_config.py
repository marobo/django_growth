from django.test import SimpleTestCase, override_settings

from django_growth.config import (
    ENV_PRODUCTION,
    get_growth_config,
    growth_config_from_mapping,
)
from django_growth.defaults import ENV_DEVELOPMENT


class GrowthConfigTests(SimpleTestCase):
    @override_settings(GROWTH={}, DEBUG=True)
    def test_empty_growth_debug_true_env_development(self):
        c = get_growth_config()
        self.assertEqual(c.env, ENV_DEVELOPMENT)
        self.assertTrue(c.robots_disallow_all)

    @override_settings(GROWTH={}, DEBUG=False)
    def test_empty_growth_debug_false_env_production(self):
        c = get_growth_config()
        self.assertEqual(c.env, ENV_PRODUCTION)
        self.assertFalse(c.robots_disallow_all)

    @override_settings(
        GROWTH={
            "GTM_ID": " GTM-ABC ",
            "SITE_NAME": " Acme ",
            "ENV": "staging",
            "GOOGLE_VERIFICATION": " abc123 ",
            "SITEMAPS": {"x": object()},
            "ROBOTS_DISALLOW_ALL": False,
            "ROBOTS_INCLUDE_SITEMAP": False,
        },
        DEBUG=True,
    )
    def test_explicit_values_normalized(self):
        c = get_growth_config()
        self.assertEqual(c.gtm_id, "GTM-ABC")
        self.assertEqual(c.site_name, "Acme")
        self.assertEqual(c.env, "staging")
        self.assertEqual(c.google_verification, "abc123")
        self.assertIn("x", c.sitemaps)
        self.assertFalse(c.robots_disallow_all)
        self.assertFalse(c.robots_include_sitemap)

    @override_settings(GROWTH={"GTM_ID": "GTM-1"}, DEBUG=False)
    def test_gtm_snippets_enabled(self):
        c = get_growth_config()
        self.assertTrue(c.gtm_snippets_enabled)

    @override_settings(GROWTH={"GTM_ID": "", "ENV": ENV_PRODUCTION}, DEBUG=False)
    def test_gtm_snippets_disabled_without_id(self):
        c = get_growth_config()
        self.assertFalse(c.gtm_snippets_enabled)

    @override_settings(GROWTH={"GTM_ID": "GTM-1", "ENV": ENV_DEVELOPMENT}, DEBUG=False)
    def test_gtm_snippets_disabled_non_production(self):
        c = get_growth_config()
        self.assertFalse(c.gtm_snippets_enabled)

    def test_growth_not_dict_treated_as_empty(self):
        with override_settings(GROWTH="bad", DEBUG=True):
            c = get_growth_config()
            self.assertEqual(c.gtm_id, "")
            self.assertEqual(c.env, ENV_DEVELOPMENT)

    def test_growth_config_from_mapping(self):
        c = growth_config_from_mapping({"ENV": ENV_PRODUCTION, "GTM_ID": "x"}, debug=False)
        self.assertEqual(c.env, ENV_PRODUCTION)
        self.assertTrue(c.gtm_snippets_enabled)

    @override_settings(GROWTH={"SITEMAPS": "nope"}, DEBUG=True)
    def test_invalid_sitemaps_becomes_empty_dict(self):
        c = get_growth_config()
        self.assertEqual(c.sitemaps, {})
