from django.template import RequestContext


def api_keys(request):
    from django.conf import settings
    return {
        'google_loader_key': settings.GOOGLELOADERKEY,
    }

