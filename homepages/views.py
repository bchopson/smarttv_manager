from django.core import serializers
from django.http import HttpResponse
from django.template import loader

from homepages.models import Slide

def index(request, tv_id):
    slides = Slide.objects.filter(tv__id=int(tv_id))
    # TODO: Change this to use rest api instead...
    slides_json = serializers.serialize('json', slides, fields=('url', 'duration'))
    template = loader.get_template('homepages/index.html')
    context = {
        'slides': slides_json,
    }
    return HttpResponse(template.render(context, request))

