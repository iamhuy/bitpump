from __future__ import unicode_literals
from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    full_name = serializers.CharField()
    image = serializers.ImageField()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserInfoUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    attributes = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)


