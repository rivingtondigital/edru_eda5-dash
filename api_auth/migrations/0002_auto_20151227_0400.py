# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 04:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtoken',
            name='renewed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='ip_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='issued',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='token',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='user',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
