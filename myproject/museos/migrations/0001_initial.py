# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('texto', models.TextField()),
                ('fecha', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('titulo_pag', models.CharField(max_length=64)),
                ('tamano', models.IntegerField()),
                ('letra', models.CharField(max_length=64)),
                ('color', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('idEntidad', models.IntegerField()),
                ('nombre', models.CharField(max_length=64)),
                ('descripcion', models.TextField()),
                ('horario', models.TextField()),
                ('transporte', models.TextField()),
                ('accesibilidad', models.BinaryField()),
                ('contentURL', models.URLField()),
                ('distrito', models.CharField(max_length=32)),
                ('telefono', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Seleccion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
    ]
