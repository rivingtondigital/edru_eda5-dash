# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_auth', '0003_auto_20151227_0406'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('write', models.BooleanField(default=False)),
                ('owner', models.BooleanField(default=False)),
                ('instrument', models.ForeignKey(to='api.DJ_Instrument', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
