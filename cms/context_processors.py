from django.conf import settings
from django.template import RequestContext

from cms.models import *

def api_keys(request):

    footer = About.objects.order_by('id').reverse()[0]
    
    if 'action' in request.GET:
        action = request.GET['action']
    else:
        action = False
    

    return {

        'google_loader_key': settings.GOOGLELOADERKEY,
        'google_analytics_key': settings.GOOGLEANALYTICSKEY,

        'footer': footer,

        'action': action,

    }

