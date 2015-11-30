# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20151128_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddFriendRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_user', models.CharField(max_length=100)),
                ('request_user', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dp', models.FileField(upload_to=myapp.models.generate_filename)),
                ('userid', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GetFriendRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_user', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='document',
            old_name='status',
            new_name='userid',
        ),
    ]
