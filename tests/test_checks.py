from django.test import SimpleTestCase, override_settings

from django_growth.checks import growth_settings_check
from django_growth.defaults import ENV_PRODUCTION


class GrowthChecksTests(SimpleTestCase):
    @override_settings(GROWTH={"ENV": ENV_PRODUCTION, "GTM_ID": ""}, DEBUG=False)
    def test_w001_production_without_gtm(self):
        warnings = growth_settings_check(None)
        ids = [w.id for w in warnings]
        self.assertIn("django_growth.W001", ids)

    @override_settings(
        GROWTH={"ENV": ENV_PRODUCTION, "GTM_ID": "GTM-1", "GOOGLE_VERIFICATION": "bad token"},
        DEBUG=False,
    )
    def test_w002_malformed_verification(self):
        warnings = growth_settings_check(None)
        ids = [w.id for w in warnings]
        self.assertIn("django_growth.W002", ids)

    @override_settings(
        GROWTH={
            "ENV": ENV_PRODUCTION,
            "GTM_ID": "GTM-1",
            "GOOGLE_VERIFICATION": "",
        },
        DEBUG=False,
    )
    def test_no_warnings_when_valid(self):
        warnings = growth_settings_check(None)
        self.assertEqual(warnings, [])
