# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import common.field


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=128)),
            ],
            options={
                'db_table': 'attribute_tab',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('email', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('salt', models.CharField(max_length=64)),
                ('password_hash', models.CharField(max_length=64)),
                ('image', models.ImageField(max_length=255, null=True, upload_to=b'profile/')),
                ('total_point', models.BigIntegerField()),
            ],
            options={
                'db_table': 'user_tab',
            },
        ),
        migrations.CreateModel(
            name='UserAttribute',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('value', models.CharField(default=b'0', max_length=128)),
                ('attribute', models.ForeignKey(db_constraint=False, to='app_user.Attribute', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False)),
                ('user', models.ForeignKey(db_constraint=False, to='app_user.User', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False)),
            ],
            options={
                'db_table': 'user_attribute_tab',
            },
        ),
    ]
