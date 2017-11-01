# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 23:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VocableStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen_count', models.IntegerField(default=0)),
                ('correct_count', models.IntegerField(default=0)),
                ('tries_count', models.IntegerField(default=0)),
                ('vocable', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vocables.Vocable')),
            ],
        ),
    ]