from django.core import serializers
from django.http import HttpResponse
from django.template import loader
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from homepages.models import Slide, Tv
from homepages.serializers import TvSerializer, SlideSerializer, SlideChildSerializer


def homepage(request, tv_id):
    slides = Slide.objects.filter(tv__id=int(tv_id))
    slides_json = serializers.serialize('json', slides, fields=('url', 'duration'))
    template = loader.get_template('homepages/homepage.html')
    context = {
        'slides': slides_json,
        'tv_id': tv_id,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    # TODO: provide list of TVs from db
    tvs = Tv.objects.all()
    template = loader.get_template('homepages/index.html')
    context = {
        'tvs': tvs,
    }
    return HttpResponse(template.render(context, request))

def editor(request):
    template = loader.get_template('homepages/editor.html')
    return HttpResponse(template.render(request))


def readme(request):
    template = loader.get_template('homepages/readme.html')
    return HttpResponse(template.render(request))

class TvList(APIView):
    """
    List all Tvs, or create a new Tv.
    """
    def get(self, request):
        tvs = Tv.objects.all()
        serializer = TvSerializer(tvs, many=True)
        return JSONResponse(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TvSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


class TvDetail(APIView):
    """
    Retrieve, update or delete a tv.
    """
    def get_object(self, pk):
        try:
            return Tv.objects.get(pk=pk)
        except Tv.DoesNotExist:
            return HttpResponse(status=404)

    def get(self, request, pk):
        tv = self.get_object(pk)
        serializer = TvSerializer(tv)
        return JSONResponse(serializer.data)

    def put(self, request, pk):
        tv = self.get_object(pk)
        data = JSONParser().parse(request)
        serializer = TvSerializer(tv, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        tv = self.get_object(pk)
        tv.delete()
        return HttpResponse(status=204)


class SlideList(APIView):
    """
    Retrieve or create slides for a given TV
    """
    def get_list(self, pk):
        try:
            return Slide.objects.filter(tv__id=pk)
        except Tv.DoesNotExist:
            return HttpResponse(status=404)

    def get(self, request, pk):
        slides = self.get_list(pk)
        serializer = SlideSerializer(slides, many=True)
        return JSONResponse(serializer.data)

    def post(self, request, pk):
        data = JSONParser().parse(request)
        serializer = SlideChildSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save(tv=Tv.objects.get(id=pk))
            return JSONResponse(serializer.data, status=201)

        return JSONResponse(serializer.errors, status=400)

    def delete(self, request, pk):
        Slide.objects.filter(tv__id=pk).delete()
        return HttpResponse(status=204)


class SlideDetail(APIView):
    """
    Retrieve, update or delete a slide.
    """
    def get_object(self, pk, idx):
        try:
            tv = Tv.objects.get(pk=pk)
            return Slide.objects.get(index=idx, tv=tv)
        except (Tv.DoesNotExist, Slide.DoesNotExist):
            return HttpResponse(status=404)

    def get(self, request, pk, idx):
        slide = self.get_object(pk, idx)
        serializer = SlideSerializer(slide)
        return JSONResponse(serializer.data)

    def put(self, request, pk, idx):
        data = JSONParser().parse(request)
        slide = self.get_object(pk, idx)
        serializer = SlideSerializer(slide, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    def delete(self, request, pk, idx):
        slide = self.get_object(pk, idx)
        try:
            slide.delete()
            return HttpResponse(status=204)
        except (Tv.DoesNotExist, Slide.DoesNotExist):
            return HttpResponse(status=404)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
