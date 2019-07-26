import hashlib, uuid
from django.db import transaction
from rest_framework.parsers import MultiPartParser

from common.views import BaseApiView
from common.exceptions import DuplicateUserEmailException, ObjectNotFoundException, InputIsInvalidException

from . import serializers
from . import models


class UserRegisterView(BaseApiView):
    permission_classes = ()
    parser_classes = (MultiPartParser,)
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            with transaction.atomic():
                user = models.User.objects.select_for_update(email=data['email'])
                if user:
                    raise DuplicateUserEmailException()
                salt = uuid.uuid4().hex
                password_hash = hashlib.sha256(request['password'] + user.salt).hexdigest()
                user = models.User(
                    email=data['email'],
                    full_name=data['full_name'],
                    salt=salt,
                    password_hash=password_hash,
                    image=data['image'],
                )
                user.save()
                request.session['uid'] = user.id
                return self.reply()
        else:
            return self.input_invalid(serializer)


class UserLoginView(BaseApiView):
    permission_classes = ()
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            user = models.User.objects.filter(email=data['email'])
            if not user:
                raise ObjectNotFoundException()
            if hashlib.sha256(request['password'] + user.salt).hexdigest() != user.password_hash:
                raise InputIsInvalidException()
            request.session['uid'] = user.id
            return self.reply()
        else:
            return self.input_invalid(serializer)


class UserInfoUpdateView(BaseApiView):
    serializer_class = serializers.UserInfoUpdateSerializer

    def post_valid(self, serializer):
        data = serializer.validated_data

        with transaction.atomic():
            user = models.User.objects.filter(id=self.uid)
            self.copy_to_db(data, user, field_list=['full_name'])
            image = data.get('file')
            if image:
                user.image = image
            user.save()
            if data.attribute_ids:
                models.UserAttribute.objects.filter(user=user).delete()
                attributes = models.Attribute.objects.filter(id__in=data.attribute_ids)
                for attribute in attributes:
                    user_attribute = models.UserAttribute(
                        user=user,
                        attribute=attribute
                    )
                    user_attribute.save()
        return self.reply()


class UserInfoGetView(BaseApiView):
    serializer_class = serializers.UserLoginSerializer

    def get_valid(self, serializer):
        user = models.User.objects.filter(id=self.uid)
        user_attributes = models.UserAttribute.objects.filter(user=user)
        return {
            'user': {
                'email': user.email,
                'full_name': user.full_name,
                'image': user.image
            },
            'attribute': [
                {
                    'id': user_attribute.attribute.id,
                    'name': user_attribute.attribute.name,
                }
                for user_attribute in user_attributes
            ]
        }


