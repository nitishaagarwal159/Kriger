# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-20 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180120_0035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Onetimelinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
    ]
