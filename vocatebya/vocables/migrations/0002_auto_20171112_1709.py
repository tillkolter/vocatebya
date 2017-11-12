# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 17:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import vocables.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vocables', '0001_initial'),
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
            name='VocableStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen_count', models.IntegerField(default=0)),
                ('correct_count', models.IntegerField(default=0)),
                ('tries_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vocable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='vocables.Vocable')),
            ],
        ),
        migrations.CreateModel(
            name='VocableTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(null=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('is_solved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(vocables.models.TimeStampsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VocableTestAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL)),
                ('vocable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='vocables.TestVocable')),
            ],
            bases=(vocables.models.TimeStampsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='testvocable',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vocables', to='vocables.VocableTest'),
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