# Generated by Django 3.0.5 on 2020-08-28 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exsite', '0012_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(default='', max_length=50000),
        ),
    ]