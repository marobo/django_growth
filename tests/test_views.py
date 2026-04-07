from django.contrib.sites.models import Site
from django.test import Client, TestCase, override_settings


class GrowthURLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Site.objects.update_or_create(
            pk=1,
            defaults={"domain": "example.com", "name": "example.com"},
        )

    def setUp(self):
        self.client = Client()

    @override_settings(GROWTH={"ROBOTS_DISALLOW_ALL": False}, DEBUG=False)
    def test_robots_txt_ok(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        self.assertIn("public", response["Cache-Control"])
        self.assertIn(b"Sitemap:", response.content)

    @override_settings(GROWTH={"ROBOTS_DISALLOW_ALL": False}, DEBUG=False)
    def test_robots_txt_head_ok(self):
        get_response = self.client.get("/robots.txt")
        head_response = self.client.head("/robots.txt")
        self.assertEqual(head_response.status_code, 200)
        self.assertEqual(head_response.content, b"")
        self.assertEqual(head_response["Content-Length"], str(len(get_response.content)))

    @override_settings(GROWTH={}, DEBUG=False)
    def test_sitemap_xml_ok(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"urlset", response.content.lower())
