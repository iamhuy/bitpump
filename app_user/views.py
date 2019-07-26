import hashlib, uuid
import json
import os
from django.db import transaction
from rest_framework.parsers import MultiPartParser

from common.views import BaseApiView
from common.image_upload import image_upload
from common.exceptions import DuplicateUserEmailException, ObjectNotFoundException, InputIsInvalidException

from . import serializers
from . import models

from activity.image_verifier import ImageVerifier


class UserRegisterView(BaseApiView):
    http_method_names = ['post']

    permission_classes = ()
    parser_classes = (MultiPartParser,)
    serializer_class = serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            with transaction.atomic():
                user = models.User.objects.select_for_update().filter(email=data['email'])
                if user:
                    raise DuplicateUserEmailException()
                salt = uuid.uuid4().hex
                password_hash = hashlib.sha256(data['password'] + salt).hexdigest()
                user = models.User(
                    email=data['email'],
                    full_name=data['full_name'],
                    salt=salt,
                    password_hash=password_hash,
                    image=data['image'],
                    total_point=0,
                    azure_person_id='',
                )
                image_url = image_upload(os.path.basename(user.image.path), user.image.path)
                person_id = ImageVerifier.add_face(user.full_name, image_url)
                user.azure_person_id = person_id
                user.save()

                request.session['uid'] = user.id
                return self.reply()
        else:
            return self.input_invalid(serializer)


class UserLoginView(BaseApiView):
    http_method_names = ['post']

    permission_classes = ()
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            user = models.User.objects.filter(email=data['email']).first()
            if not user:
                raise ObjectNotFoundException()
            if hashlib.sha256(data['password'] + user.salt).hexdigest() != user.password_hash:
                raise InputIsInvalidException()
            request.session['uid'] = user.id
            return self.reply()
        else:
            return self.input_invalid(serializer)


class UserInfoUpdateView(BaseApiView):
    http_method_names = ['post']
    parser_classes = (MultiPartParser,)
    serializer_class = serializers.UserInfoUpdateSerializer

    def post_valid(self, serializer):
        data = serializer.validated_data

        with transaction.atomic():
            db_user = models.User.objects.filter(id=self.uid).first()
            self.copy_to_db(data, db_user, field_list=['full_name'])
            image = data.get('file')
            if image:
                db_user.image = image
                db_user.save()
            if data['attributes']:
                attributes = [json.loads(attribute) for attribute in data['attributes']]
                attribute_id_attribute = {attribute['id']: attribute for attribute in attributes}
                models.UserAttribute.objects.filter(user=db_user).delete()
                db_attributes = models.Attribute.objects.filter(id__in=attribute_id_attribute.keys())
                for db_attribute in db_attributes:
                    user_attribute = models.UserAttribute(
                        user=db_user,
                        attribute=db_attribute,
                        value=attribute_id_attribute[db_attribute.id]['value']
                    )
                    user_attribute.save()
        return self.reply()


class UserInfoGetView(BaseApiView):
    http_method_names = ['get']
    serializer_class = serializers.UserLoginSerializer

    def get_valid(self, serializer):
        user = models.User.objects.filter(id=self.uid).first()
        user_attributes = models.UserAttribute.objects.filter(user=user)
        return self.reply({
            'user': {
                'email': user.email,
                'full_name': user.full_name,
                'image': user.image.url
            },
            'attributes': [
                {
                    'id': user_attribute.attribute.id,
                    'name': user_attribute.attribute.name,
                    'value': user_attribute.value,
                }
                for user_attribute in user_attributes
            ]
        })


class AttributeGetView(BaseApiView):
    http_method_names = ['get']
    serializer_class = serializers.UserLoginSerializer

    def get_valid(self, serializer):
        attributes = models.Attribute.objects.all()
        return self.reply({
            'attributes': [
                {
                    'id': attribute.id,
                    'name': attribute.name,
                }
                for attribute in attributes
            ]
        })



