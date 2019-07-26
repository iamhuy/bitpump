import time
from rest_framework.parsers import MultiPartParser

from common.views import BaseApiView
from common import exceptions

from . import serializers
from . import models


class ActivityCategoryGetView(BaseApiView):
    http_method_names = ['get']

    def get_valid(self, serializer):
        activity_categories = models.ActivityCategory.objects.all()
        return self.reply({
            'activity_categories': [
                {
                    'id': activity_category.id,
                    'name': activity_category.name,
                    'complete_point': activity_category.complete_point,
                    'fail_point': activity_category.fail_point,
                }
                for activity_category in activity_categories
            ]
        })


class LuckyDrawUpdateView(BaseApiView):
    http_method_names = ['post']
    serializer_class = serializers.LuckyDrawUpdateSerializer

    def post_valid(self, serializer):
        data = serializer.data
        db_user = models.User.objects.filter(id=self.uid).first()
        lucky_draw = models.UserLuckyDraw.objects.filter(user=db_user,
                                                         status__in=[
                                                             models.UserLuckyDraw.STATUS_INIT,
                                                             models.UserLuckyDraw.STATUS_ACCEPTED,
                                                         ])
        if lucky_draw:
            raise exceptions.InputIsInvalidException()

        db_activity_category = models.ActivityCategory.objects.filter(
            id=data['activity_category_id']
        ).first()
        if not db_activity_category:
            raise exceptions.ObjectNotFoundException()

        result = models.UserLuckyDraw(
            user=db_user,
            activity_category=db_activity_category,
            add_time=time.time(),
            upd_time=time.time(),
            status=data['status']
        )
        result.save()
        return self.reply()


class LuckyDrawGetView(BaseApiView):
    http_method_names = ['get']

    def get_valid(self, serializer):
        db_user = models.User.objects.filter(id=self.uid).first()
        lucky_draw = models.UserLuckyDraw.objects.filter(user=db_user,
                                                         status__in=[
                                                             models.UserLuckyDraw.STATUS_INIT,
                                                             models.UserLuckyDraw.STATUS_ACCEPTED,
                                                             models.UserLuckyDraw.STATUS_MATCHED,
                                                         ]).first()
        if not lucky_draw:
            return self.reply()

        return self.reply({
            'activity_category': {
                'id': lucky_draw.activity_category.id,
                'name': lucky_draw.activity_category.name,
            },
            'status': lucky_draw.status
        })


class ActivityUpdateView(BaseApiView):
    http_method_names = ['post']
    serializer_class = serializers.ActivityUpdateSerializer

    def post_valid(self, serializer):
        data = serializer.validated_data
        db_user = models.User.objects.filter(id=self.uid).first()
        db_user_activity = models.UserActivity.objects.filter(user=db_user,
                                                              activity__status__in=[
                                                                  models.Activity.STATUS_INIT,
                                                              ],
                                                              activity__id=data['activity_id']).first()
        if not db_user_activity:
            raise exceptions.ObjectNotFoundException()

        if data['status'] != models.Activity.STATUS_COMPLETED:
            db_user_activity.activity.status = data['status']

        # verify location
        # verify image
        return self.reply()


class ActivityImageUploadView(BaseApiView):
    http_method_names = ['post']
    parser_classes = (MultiPartParser,)
    serializer_class = serializers.ActivityImageUploadSerializer

    def post_valid(self, serializer):
        data = serializer.validated_data
        db_user = models.User.objects.filter(id=self.uid).first()
        db_user_activity = models.UserActivity.objects.filter(user=db_user,
                                                              activity__status__in=[
                                                                  models.Activity.STATUS_INIT,
                                                              ],
                                                              activity__id=data['activity_id']).first()
        if not db_user_activity:
            raise exceptions.ObjectNotFoundException()

        activity_image = models.ActivityImage(
            activity=db_user_activity.activity,
            image=data['image']
        )
        activity_image.save()
        return self.reply()


class ActivityGetView(BaseApiView):
    http_method_names = ['get']

    def get_valid(self, serializer):
        db_user = models.User.objects.filter(id=self.uid).first()
        user_activities = models.UserActivity.objects.filter(user=db_user,
                                                             activity__status__in=[
                                                                 models.Activity.STATUS_INIT,
                                                                 models.Activity.STATUS_COMPLETED,
                                                             ])

        return self.reply({
            'activities': [
                {
                    'id': user_activity.activity.id,
                    'activity_category': {
                        'id': user_activity.activity.activity_category.id,
                        'name': user_activity.activity.activity_category.name
                    },
                    'users': [
                        {
                            "id": user_activity.user.id,
                            "full_name": user_activity.user.full_name,
                            "image": user_activity.user.image.url,
                        }
                        for user_activity in models.UserActivity.objects.filter(activity=user_activity.activity)
                    ],
                    'location': {
                        'latitude': user_activity.activity.latitude,
                        'longitude': user_activity.activity.longitude
                    },
                    'images': {
                        activity_image.image.url
                        for activity_image in models.ActivityImage.objects.filter(activity=user_activity.activity)
                    },
                    'expiry_time': user_activity.activity.expiry_time,
                    'status': user_activity.activity.status,
                }
                for user_activity in user_activities
            ]
        })
