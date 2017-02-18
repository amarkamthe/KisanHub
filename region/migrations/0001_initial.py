# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import jsonfield.fields
from sys import path
from django.core import serializers
import os

fixture_filename = 'region.json'
def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_filename)

    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
    for obj in objects:
        obj.save()
    fixture.close()

def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    MyModel = apps.get_model("region", "region")
    MyModel.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('file_name', models.CharField(max_length=1024)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='region.Region', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatisticalData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('component', models.CharField(max_length=1, choices=[(b'1', b'Tmin'), (b'2', b'Tmax'), (b'3', b'Tmean'), (b'4', b'Sunshine')])),
                ('blob', jsonfield.fields.JSONField(default=dict)),
                ('region', models.ForeignKey(to='region.Region')),
            ],
        ),
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
