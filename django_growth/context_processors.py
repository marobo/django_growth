from django_growth.config import get_growth_config_for_request


def growth(request):
    config = get_growth_config_for_request(request)
    return {"growth": config.as_template_context()}
