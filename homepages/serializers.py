from rest_framework import serializers
from homepages.models import Tv, Slide


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ('tv', 'index', 'url', 'duration')

class SlideChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ('index', 'url', 'duration')

class TvSerializer(serializers.ModelSerializer):
    slides = SlideChildSerializer(many=True)

    class Meta:
        model = Tv
        fields = ('id', 'ip_address', 'updated', 'slides')