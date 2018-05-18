# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0002_auto_20180516_1658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='museo',
            options={'ordering': ['nombre']},
        ),
        migrations.RemoveField(
            model_name='museo',
            name='numero_comentarios',
        ),
    ]
