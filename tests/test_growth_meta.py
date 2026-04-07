from django.template import Context, Template
from django.test import RequestFactory, TestCase, override_settings


class GrowthMetaTagTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/blog/post/")

    @override_settings(GROWTH={"DEFAULT_OG_IMAGE": "https://cdn.example/default.png"})
    def test_og_image_falls_back_to_growth_default(self):
        html = Template("{% load growth_tags %}{% growth_meta title='Hello' %}").render(
            Context({"request": self.request})
        )
        self.assertIn('property="og:image"', html)
        self.assertIn("https://cdn.example/default.png", html)

    @override_settings(GROWTH={"DEFAULT_OG_IMAGE": "https://cdn.example/default.png"})
    def test_explicit_og_image_overrides_default(self):
        html = Template(
            "{% load growth_tags %}{% growth_meta title='Hello' og_image='https://x/y.png' %}"
        ).render(Context({"request": self.request}))
        self.assertIn("https://x/y.png", html)
        self.assertNotIn("https://cdn.example/default.png", html)

    @override_settings(GROWTH={})
    def test_twitter_card_summary_when_no_image(self):
        html = Template("{% load growth_tags %}{% growth_meta title='Hi' %}").render(
            Context({"request": self.request})
        )
        self.assertIn('name="twitter:card" content="summary"', html)
