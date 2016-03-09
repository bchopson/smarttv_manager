from django.core import serializers
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from homepages.models import Slide, Tv
from homepages.serializers import TvSerializer, SlideSerializer, SlideChildSerializer


def index(request, tv_id):
    slides = Slide.objects.filter(tv__id=int(tv_id))
    # TODO: Change this to use rest api instead...
    slides_json = serializers.serialize('json', slides, fields=('url', 'duration'))
    template = loader.get_template('homepages/index.html')
    context = {
        'slides': slides_json,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def tv_list(request):
    """
    List all Tvs, or create a new Tv.
    """
    if request.method == 'GET':
        tvs = Tv.objects.all()
        serializer = TvSerializer(tvs, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TvSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def tv_detail(request, pk):
    """
    Retrieve, update or delete a Tv.
    """
    try:
        tv = Tv.objects.get(pk=pk)
    except Tv.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TvSerializer(tv)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TvSerializer(tv, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        tv.delete()
        return HttpResponse(status=204)


# Not adding bulk delete for now
@csrf_exempt
def slides(request, pk):
    """
    Retrieve, update or delete slides for a given TV
    """
    try:
        slides = Slide.objects.filter(tv__id=pk)
    except Tv.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SlideSerializer(slides, many=True)
        return JSONResponse(serializer.data)

    # bulk update
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SlideChildSerializer(slides, data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)