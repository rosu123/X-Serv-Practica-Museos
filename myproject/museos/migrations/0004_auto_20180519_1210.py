# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-19 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0003_auto_20180518_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='barrio',
            field=models.CharField(default='-', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='claseVial',
            field=models.CharField(default='-', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='codPostal',
            field=models.CharField(default='-', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='localidad',
            field=models.CharField(default='-', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='nombreVia',
            field=models.CharField(default='-', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='numero',
            field=models.CharField(default='-', max_length=8),
            preserve_default=False,
        ),
    ]
