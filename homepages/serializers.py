from rest_framework import serializers
from homepages.models import Tv


class TvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tv
        fields = ('id', 'ip_address', 'updated')
