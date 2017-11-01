# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 13:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(3, 'Determiner'), (1, 'Noun'), (2, 'Verb')])),
                ('word', models.CharField(max_length=64)),
                ('features', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
            ],
        ),
    ]
