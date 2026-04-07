# django-growth

Reusable Django tooling for **Google Tag Manager**, **SEO meta tags** (including Open Graph), **Google Search Console** verification, **`robots.txt`**, and **`sitemap.xml`**—with environment-aware defaults and minimal project wiring.

## Features

- **Google Tag Manager** — Head and body snippets via template tags; loads only when `ENV` is `production` and `GTM_ID` is set.
- **SEO meta** — Title, description, canonical URL, Open Graph, Twitter cards, optional `robots` meta.
- **Search Console** — Optional `google-site-verification` meta tag when a token is configured.
- **`robots.txt`** — Dynamic `Sitemap:` URL; optional disallow-all for non-production or explicit override.
- **Sitemaps** — Django’s built-in sitemap framework with a project-supplied `SITEMAPS` registry (falls back to a valid empty sitemap if unset).
- **Context processor** — Normalized `growth` dict in templates (`GTM_ID`, `SITE_NAME`, `ENV`, `GOOGLE_VERIFICATION`).
- **Frontend analytics** — `dataLayer` bootstrap and global `trackEvent(name, data)` for GTM-friendly custom events.
- **Configuration layer** — `GrowthConfig` / `get_growth_config()` single source of truth for `GROWTH`; template tags and views stay thin.
- **System checks** — Warnings for production-without-GTM and suspicious verification tokens (`django_growth.W001`, `W002`).

## Requirements

- Python 3.10+
- Django 4.2+

## Public contract (stable API)

These names and shapes are intended to stay stable across minor releases:

| Surface | Contract |
|--------|-----------|
| **Settings** | `GROWTH` dict on `django.conf.settings` (see below). Unknown keys are ignored. |
| **Python** | `django_growth.config.get_growth_config()`, `get_growth_config_for_request(request)`, and `GrowthConfig` (fields + `gtm_snippets_enabled`, `as_template_context()`). |
| **Context** | `growth` mapping with `GTM_ID`, `SITE_NAME`, `ENV`, `GOOGLE_VERIFICATION`, `DEFAULT_OG_IMAGE` (from the context processor). |
| **Template tags** | `{% load growth_tags %}` → `growth_meta`, `growth_gtm`, `growth_gtm_body`, `growth_analytics`. |
| **URLs** | `path("", include("django_growth.urls"))` → `django_growth:robots_txt`, `django_growth:sitemap`. |
| **System checks** | `django_growth.W001` (production without GTM ID), `django_growth.W002` (verification token shape). |

Do not import private helpers from other modules; use `get_growth_config()` for custom code in host projects.

## Installation

Install from Git (replace the URL and ref with your fork or tag):

```bash
pip install "django-growth @ git+https://github.com/marobo/django_growth.git@v0.1.0"
```

Or add to `requirements.txt`:

```text
django-growth @ git+https://github.com/marobo/django_growth.git@v0.1.0
```

## Quick start

### 1. Register the app

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.sitemaps",  # required for Django’s sitemap templates (sitemap.xml)
    "django.contrib.sites",  # recommended for absolute URLs in sitemaps
    "django_growth",
]
```

If you use `django.contrib.sites`, set `SITE_ID` to the correct row in the `sites` table.

### 2. Context processor

In `TEMPLATES` → `OPTIONS` → `context_processors`:

```python
"django.request",
"django_growth.context_processors.growth",
```

### 3. Settings

```python
GROWTH = {
    "GTM_ID": "GTM-XXXXXXX",
    "SITE_NAME": "My product",
    "ENV": "production",  # omit or leave blank to infer from DEBUG when unset
    "GOOGLE_VERIFICATION": "your-google-search-console-verification-token",
    "SITEMAPS": {
        # "pages": PagesSitemap,
        # "blog": BlogSitemap,
    },
    # Site-wide default for Open Graph / Twitter image when a page omits og_image:
    # "DEFAULT_OG_IMAGE": "https://your-domain.com/static/og-default.png",
    # Optional robots behavior (defaults are safe for local dev):
    # "ROBOTS_DISALLOW_ALL": True,
    # "ROBOTS_INCLUDE_SITEMAP": True,
}
```

| Key | Type | Default / notes |
|-----|------|------------------|
| `GTM_ID` | `str` | `""` — stripped whitespace |
| `SITE_NAME` | `str` | `""` |
| `ENV` | `str` | `development` if `DEBUG` else `production` when omitted or blank |
| `GOOGLE_VERIFICATION` | `str` | `""` — HTML-tag token only |
| `DEFAULT_OG_IMAGE` | `str` | `""` — absolute URL; used by `{% growth_meta %}` when `og_image` is omitted (satisfies tools that require `og:image`) |
| `SITEMAPS` | `dict` | `{}` — section name → `Sitemap` class or instance; non-dict ignored |
| `ROBOTS_DISALLOW_ALL` | `bool` | `DEBUG` when omitted |
| `ROBOTS_INCLUDE_SITEMAP` | `bool` | `True` |

- **`ENV`**: GTM snippets render only when `ENV == "production"` and `GTM_ID` is non-empty (`GrowthConfig.gtm_snippets_enabled`).
- **`ROBOTS_DISALLOW_ALL`**: When `True`, emits `Disallow: /` and omits `Sitemap:`.
- **`DEFAULT_OG_IMAGE`**: Many crawlers and share debuggers treat `og:image` as required once other Open Graph tags are present. Set this to a default logo or hero image URL, or pass `og_image` on each `{% growth_meta %}` call.

### 4. URLs

```python
urlpatterns = [
    path("", include("django_growth.urls")),
    # ...
]
```

This exposes **`/robots.txt`** and **`/sitemap.xml`** (adjust the mount prefix if you include under a path).

#### If SEO tools report “robots.txt check failed”

- Confirm **`path("", include("django_growth.urls"))`** is active (often at the **root** of `urlpatterns` so the live URL is `https://your-domain/robots.txt`, not only under a subpath).
- Ensure the checker’s hostname is allowed (**`ALLOWED_HOSTS`** in Django, and any reverse proxy).
- With **`DEBUG = True`**, the default is **`ROBOTS_DISALLOW_ALL`** equal to **`True`** (`Disallow: /`), which is correct for local/staging but some external “verification” products still flag it. For a crawlable production site, set **`DEBUG = False`** and either omit **`ROBOTS_DISALLOW_ALL`** or set it to **`False`**.

## Usage in templates

```django
{% load growth_tags %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  {% growth_meta title=page_title description=page_description %}
  {% growth_analytics %}
  {% growth_gtm %}
</head>
<body>
  {% growth_gtm_body %}
  {% block content %}{% endblock %}
</body>
</html>
```

- Provide **`page_title`** and **`page_description`** from the view or via template blocks.
- Place **`{% growth_analytics %}`** before **`{% growth_gtm %}`** so `dataLayer` exists before the GTM bootstrap script runs.
- Place **`{% growth_gtm %}`** early in `<head>` and **`{% growth_gtm_body %}`** immediately after `<body>` per Google’s GTM documentation.
- **`{% growth_meta %}`** accepts optional arguments such as `og_image`, `canonical_url`, `robots`, and `site_title_suffix`—see the template tag implementation in your installed version.

Template context includes **`growth`** (from the context processor) with `GTM_ID`, `SITE_NAME`, `ENV`, `GOOGLE_VERIFICATION`, and `DEFAULT_OG_IMAGE`.

## Frontend analytics (`trackEvent`)

Add **`{% growth_analytics %}`** once per page (typically in `<head>`). It:

- Ensures **`window.dataLayer`** is an array (GTM-compatible).
- Defines **`window.trackEvent(name, data)`**, which pushes `{ event: name, ...data }` onto `dataLayer`.

**Example (inline HTML / template)**

```html
<button type="button" onclick="trackEvent('cta_click', { cta_id: 'signup_header' })">
  Sign up
</button>
```

**Example (vanilla JS)**

```javascript
trackEvent("purchase_complete", { value: 99, currency: "USD" });
```

In GTM, create a trigger on **Custom Event** matching the `event` name you pass as `name`, and use **Data Layer variables** for extra keys. The helper is environment-agnostic: it only pushes to `dataLayer`; whether GTM loads still follows your **`{% growth_gtm %}`** / `ENV` rules.

## Sitemaps

1. Define one or more subclasses of `django.contrib.sitemaps.Sitemap` in your project (implement `items()` and URL resolution per the Django docs).
2. Register them under **`GROWTH["SITEMAPS"]`** as a dict: section name → sitemap class or instance.
3. Ensure **`django.contrib.sites`** and **`SITE_ID`** match your deployment domain when generating absolute URLs.

If **`SITEMAPS`** is omitted or empty, **`sitemap.xml`** still responds with a valid, empty sitemap section so URLs never 500 during early setup.

## Google Search Console

**HTML tag verification**

1. In Search Console, choose the **HTML tag** verification method and copy the **content** value of the `google-site-verification` meta tag.
2. Set **`GROWTH["GOOGLE_VERIFICATION"]`** to that token (string only, not the full tag).
3. Deploy; confirm the live page’s HTML includes the meta tag (via **View Source** or “URL inspection” after indexing).

**Sitemap submission**

1. With **`django_growth.urls`** mounted, open `https://your-domain/sitemap.xml` and confirm it loads.
2. In Search Console → **Sitemaps**, submit `https://your-domain/sitemap.xml`.

**`robots.txt`**

With crawling allowed, **`robots.txt`** includes a **`Sitemap:`** line pointing at the same host’s `sitemap.xml`, which helps discovery (submission in Search Console is still recommended).

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python runtests.py
```

## License

MIT (or your chosen license—update this section to match `pyproject.toml`).
