from django.http import HttpResponse
from django.template import loader

from homepages.models import Tv


def index(request):
    tvs = Tv.objects.all()
    template = loader.get_template('smarttv_manager/index.html')
    context = {
        'tvs': tvs,
    }
    return HttpResponse(template.render(context, request))