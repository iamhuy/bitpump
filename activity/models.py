from django.db import models

from common.field import PositiveBigIntegerField, BigAutoField
from app_user.models import User


class ActivityCategory(models.Model):
    id = BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    complete_point = models.IntegerField()
    fail_point = models.IntegerField()

    class Meta:
        db_table = 'activity_category_tab'


class UserLuckyDraw(models.Model):
    id = BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)

    STATUS_INIT = 1
    STATUS_ACCEPTED = 2
    STATUS_DENIED = 3
    STATUS_MATCHED = 4
    status = models.PositiveSmallIntegerField(
        choices=(
            (STATUS_INIT, 'Init'),
            (STATUS_ACCEPTED, 'Accepted'),
            (STATUS_DENIED, 'Denied'),
            (STATUS_MATCHED, 'Matched'),
        ),
        default=STATUS_INIT,
    )

    class Meta:
        db_table = 'user_lucky_draw_tab'


class Activity(models.Model):
    id = BigAutoField(primary_key=True)
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    time = PositiveBigIntegerField()
    place_name = models.CharField(max_length=255, default='')
    expiry_time = PositiveBigIntegerField()

    STATUS_INIT = 1
    STATUS_COMPLETED = 2
    STATUS_DENIED = 3
    STATUS_EXPIRED = 4
    status = models.PositiveSmallIntegerField(
        choices=(
            (STATUS_INIT, 'Init'),
            (STATUS_COMPLETED, 'Completed'),
            (STATUS_DENIED, 'Denied'),
            (STATUS_EXPIRED, 'Expired'),
        ),
        default=STATUS_INIT,
    )

    class Meta:
        db_table = 'activity_tab'


class ActivityImage(models.Model):
    id = BigAutoField(primary_key=True)
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)
    image = models.ImageField(upload_to='activity/', null=True, max_length=255)

    class Meta:
        db_table = 'activity_image_tab'


class UserActivity(models.Model):
    id = BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)

    class Meta:
        db_table = 'user_activity_tab'
