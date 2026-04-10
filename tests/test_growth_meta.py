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

    @override_settings(
        GROWTH={
            "META_VIEWPORT": "width=device-width, initial-scale=1.0",
            "META_KEYWORDS": "one, two",
            "META_AUTHOR": "Author",
            "OG_LOCALE": "en_US",
            "TWITTER_SITE": "@site",
            "TWITTER_CREATOR": "@creator",
        }
    )
    def test_growth_meta_emits_config_meta_social_tags(self):
        html = Template(
            "{% load growth_tags %}{% growth_meta title='T' description='D' %}"
        ).render(Context({"request": self.request}))
        self.assertIn('name="viewport" content="width=device-width, initial-scale=1.0"', html)
        self.assertIn('name="keywords" content="one, two"', html)
        self.assertIn('name="author" content="Author"', html)
        self.assertIn('property="og:locale" content="en_US"', html)
        self.assertIn('name="twitter:site" content="@site"', html)
        self.assertIn('name="twitter:creator" content="@creator"', html)

    @override_settings(
        GROWTH={
            "META_KEYWORDS": "from settings",
            "TWITTER_SITE": "@settings",
        }
    )
    def test_growth_meta_tag_args_override_config(self):
        html = Template(
            "{% load growth_tags %}"
            "{% growth_meta title='T' keywords='from tag' twitter_site='@tag' %}"
        ).render(Context({"request": self.request}))
        self.assertIn('name="keywords" content="from tag"', html)
        self.assertNotIn("from settings", html)
        self.assertIn('name="twitter:site" content="@tag"', html)

    @override_settings(GROWTH={"META_KEYWORDS": "from settings"})
    def test_empty_keywords_arg_suppresses_meta_keywords(self):
        html = Template(
            "{% load growth_tags %}{% growth_meta title='T' keywords='' %}"
        ).render(Context({"request": self.request}))
        self.assertNotIn("keywords", html)
