# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PartyShiftSchedule', '0003_auto_20160822_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time',
            name='date',
        ),
        migrations.AlterField(
            model_name='time',
            name='beginning',
            field=models.DateTimeField(),
        ),
    ]
