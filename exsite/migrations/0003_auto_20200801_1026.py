# Generated by Django 3.0.5 on 2020-08-01 04:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exsite', '0002_auto_20200801_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='endtime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='question',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
