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
                    raise DuplicateUserEmailException
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
                user.save()

                image_url = image_upload(os.path.basename(user.image.path), user.image.path)
                person_id = ImageVerifier.add_face(user.full_name, image_url)
                user.azure_person_id = person_id
                user.save()

                age_attr = models.Attribute.objects.get(name='Age')
                gender_attr = models.Attribute.objects.get(name='Gender')
                team_attr = models.Attribute.objects.get(name='Team')

                models.UserAttribute.objects.bulk_create([
                    models.UserAttribute(user=user, attribute=age_attr, value=str(data['age'])),
                    models.UserAttribute(user=user, attribute=gender_attr, value=data['gender']),
                    models.UserAttribute(user=user, attribute=team_attr, value=data['team']),
                ])
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
                raise ObjectNotFoundException
            if hashlib.sha256(data['password'] + user.salt).hexdigest() != user.password_hash:
                raise InputIsInvalidException
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
        ignore_attr_ids = list(
            models.Attribute.objects.filter(name__in=['Age', 'Gender', 'Team']).values_list('id', flat=True))

        with transaction.atomic():
            db_user = models.User.objects.filter(id=self.uid).first()
            self.copy_to_db(data, db_user, field_list=['full_name'])
            image = data.get('file')
            if image:
                db_user.image = image
                db_user.save()
            if data['attributes']:
                attributes = [json.loads(attribute) for attribute in data['attributes']]
                attribute_id_attribute = {attribute['id']: attribute for attribute in attributes
                                          if attribute['id'] not in ignore_attr_ids}
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


class UserRankingGetView(BaseApiView):
    http_method_names = ['get']
    permission_classes = ()

    def get_valid(self, serializer):
        users = models.User.objects.order_by('-total_point')[:10]
        return self.reply({
            'ranking': [
                {
                    'image': user.image.url,
                    'point': user.total_point,
                    'name': user.full_name
                }
                for user in users
            ]
        })


class UserConnectionGetView(BaseApiView):
    http_method_names = ['get']
    permission_classes = ()

    def get_valid(self, serializer):
        import matplotlib.pyplot as plt
        import networkx as nx
        import time
        import datetime
        from django.conf import settings
        from activity import models as activity_models

        now = datetime.datetime.now()
        image_name = settings.MEDIA_ROOT + "/connections/connections_%s_%s_%s.png" % (now.year, now.month, now.day)
        image_url = settings.MEDIA_URL + "connections/connections_%s_%s_%s.png" % (now.year, now.month, now.day)
        if os.path.exists(image_name):
            return self.reply({
                'image': image_url
            })
        available_users = models.User.objects.all()
        user_activities = activity_models.UserActivity.objects.filter(
            activity__time__gt=time.time() - 30 * 24 * 3600,
            activity__status=activity_models.Activity.STATUS_COMPLETED
        )

        activity_users_list = {}
        for user_activity in user_activities:
            activity_users_list.setdefault(user_activity.activity, []).append(user_activity.user)

        users_map = {}  # {(u1, u2): weight}
        for users in activity_users_list.values():
            users_map.setdefault((users[0], users[1]), 0)
            users_map[(users[0], users[1])] += 1

        graph = nx.DiGraph()  # Create a graph object called G
        for users, weight in users_map.items():
            graph.add_edges_from(
                [(users[0].id, users[1].id)], weight=weight
            )
        company_total_point = 0
        for user in available_users:
            company_total_point += user.total_point

        values = {user.id: str(float(user.total_point) / float(company_total_point))
                  for user in available_users}
        values = [values.get(node, 0.45) for node in graph.nodes()]

        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in graph.edges(data=True)])

        node_labels = {user.id: user.full_name for user in available_users}
        edge_colors = ['black' for _ in graph.edges()]
        pos = nx.spring_layout(graph)
        nx.draw_networkx_labels(graph, pos, node_labels, font_size=11)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        nx.draw(graph, pos, node_color=values, node_size=3500, edge_color=edge_colors, arrows=False)

        # Plot the graph
        plt.title('Company Connections')
        plt.axis('off')
        plt.savefig(image_name)

        return self.reply({
            'image': image_url
        })
