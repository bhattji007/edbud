# Generated by Django 3.0.5 on 2020-08-01 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exsite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='endtime',
        ),
        migrations.RemoveField(
            model_name='question',
            name='starttime',
        ),
    ]