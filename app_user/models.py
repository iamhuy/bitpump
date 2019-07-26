from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile/', null=True, max_length=255)
    total_point = models.BigIntegerField()

    class Meta:
        db_table = 'user_tab'


class Attribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128, default='')

    class Meta:
        db_table = 'attribute_tab'


class UserAttribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)
    attribute = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, db_index=False)

    class Meta:
        db_table = 'user_attribute_tab'
