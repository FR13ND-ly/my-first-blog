# Generated by Django 3.0.8 on 2020-12-24 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0087_auto_20200913_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='photo_of_user',
        ),
    ]
