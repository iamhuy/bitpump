# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import common.field
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('longitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('latitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('time', common.field.PositiveBigIntegerField()),
                ('expiry_time', common.field.PositiveBigIntegerField()),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Init'), (2, b'Completed'), (3, b'Rejected'), (4, b'Expired')])),
            ],
            options={
                'db_table': 'activity_2_tab',
            },
        ),
        migrations.CreateModel(
            name='ActivityCategory',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('complete_point', models.IntegerField()),
                ('fail_point', models.IntegerField()),
            ],
            options={
                'db_table': 'activity_category_tab',
            },
        ),
        migrations.CreateModel(
            name='ActivityImage',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('image', models.ImageField(max_length=255, null=True, upload_to=b'activity/')),
                ('activity', models.ForeignKey(db_constraint=False, to='activity.Activity', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False)),
            ],
            options={
                'db_table': 'activity_image_tab',
            },
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('activity', models.ForeignKey(db_constraint=False, to='activity.Activity', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False)),
                ('user', models.ForeignKey(db_constraint=False, to='app_user.User', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False)),
            ],
            options={
                'db_table': 'user_activity_tab',
            },
        ),
        migrations.CreateModel(
            name='UserLuckyDraw',
            fields=[
                ('id', common.field.BigAutoField(serialize=False, primary_key=True)),
                ('add_time', common.field.PositiveBigIntegerField()),
                ('upd_time', common.field.PositiveBigIntegerField()),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(1, b'Init'), (2, b'Accepted'), (3, b'Denied'), (4, b'Matched')])),
                ('activity', models.ForeignKey(db_constraint=False, to='activity.ActivityCategory', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False)),
                ('user', models.ForeignKey(db_constraint=False, to='app_user.User', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False)),
            ],
            options={
                'db_table': 'user_lucky_draw_tab',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_category',
            field=models.ForeignKey(db_constraint=False, to='activity.ActivityCategory', on_delete=django.db.models.deletion.DO_NOTHING, db_index=False),
        ),
    ]
