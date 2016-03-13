# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DJ_Instrument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instrument_id', models.IntegerField()),
                ('name', models.CharField(max_length=512, null=True)),
                ('shortname', models.CharField(max_length=512, null=True)),
                ('major_version', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
