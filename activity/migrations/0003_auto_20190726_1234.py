# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20190726_1212'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='activity',
            table='activity_tab',
        ),
    ]
