# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20190726_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='place_name',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
