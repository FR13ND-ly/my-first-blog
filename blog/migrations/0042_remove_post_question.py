# Generated by Django 3.0.1 on 2020-02-05 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_auto_20200205_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='question',
        ),
    ]
