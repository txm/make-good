from django.conf import settings
from django.template import RequestContext

from cms.models import *

def api_keys(request):

    if About.objects.count() > 0:
        footer = About.objects.order_by('id').reverse()[0]
    else:
        footer = False
    
    if 'action' in request.GET:
        action = request.GET['action']
    else:
        action = False
    
    if 'message' in request.GET:
        message = request.GET['message']
    else:
        message = False
    

    return {

        'google_loader_key': settings.GOOGLELOADERKEY,
        'google_analytics_key': settings.GOOGLEANALYTICSKEY,

        'footer': footer,

        'action': action,
        'message': message,

    }

