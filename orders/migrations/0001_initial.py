# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('stamp_type', models.CharField(max_length=1000, null=True, blank=True)),
                ('size', models.IntegerField(blank=True, null=True, choices=[(0, b'small'), (1, b'medium'), (2, b'large')])),
                ('font', models.CharField(max_length=1000, null=True, blank=True)),
                ('color', models.CharField(max_length=1000, null=True, blank=True)),
                ('allignment', models.CharField(max_length=1000, null=True, blank=True)),
                ('rate', models.IntegerField(null=True, blank=True)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('request', models.CharField(max_length=1000, null=True, blank=True)),
                ('advance', models.IntegerField(null=True, blank=True)),
                ('delivery_date', models.DateField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('company', models.CharField(max_length=1000, null=True, blank=True)),
                ('designation', models.CharField(max_length=1000, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('address', models.CharField(max_length=1000, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
