# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-19 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0005_auto_20180519_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museo',
            name='contentURL',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='horario',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='transporte',
            field=models.TextField(null=True),
        ),
    ]