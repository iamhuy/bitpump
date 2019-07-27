from __future__ import unicode_literals
from rest_framework import serializers


class LuckyDrawUpdateSerializer(serializers.Serializer):
    activity_category_id = serializers.IntegerField()
    status = serializers.IntegerField()


class LocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(min_value=0, decimal_places=6, max_digits=20)
    longitude = serializers.DecimalField(min_value=0, decimal_places=6, max_digits=20)


class ActivityUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.IntegerField()
    lat = serializers.DecimalField(min_value=0, decimal_places=10, max_digits=20)
    long = serializers.DecimalField(min_value=0, decimal_places=10, max_digits=20)


class ActivityImageUploadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()
