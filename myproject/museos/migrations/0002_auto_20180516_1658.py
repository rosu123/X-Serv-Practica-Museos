# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='numero_comentarios',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='museo',
            name='accesibilidad',
            field=models.BooleanField(default=False),
        ),
    ]
