from django.db import models
from common.field import BigAutoField


class User(models.Model):
    id = BigAutoField(primary_key=True)
    email = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    salt = models.CharField(max_length=64)
    password_hash = models.CharField(max_length=64)
    image = models.ImageField(upload_to='profile/', null=True, max_length=255)
    total_point = models.BigIntegerField()

    class Meta:
        db_table = 'user_tab'


class Attribute(models.Model):
    id = BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, default='')

    class Meta:
        db_table = 'attribute_tab'


class UserAttribute(models.Model):
    id = BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)
    value = models.CharField(max_length=128, default='0')

    class Meta:
        db_table = 'user_attribute_tab'
