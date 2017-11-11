# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 22:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import vocables.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vocables', '0002_vocablestats'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestVocable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VocableTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            bases=(vocables.models.TimeStampsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VocableTestAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vocable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vocables.TestVocable')),
            ],
            bases=(vocables.models.TimeStampsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VocableTestStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(null=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('is_solved', models.BooleanField(default=False)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='vocables.VocableTest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='testvocable',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vocables', to='vocables.VocableTestStats'),
        ),
        migrations.AddField(
            model_name='testvocable',
            name='vocable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='vocables.Vocable'),
        ),
        migrations.AlterIndexTogether(
            name='testvocable',
            index_together=set([('test', 'position', 'vocable')]),
        ),
    ]