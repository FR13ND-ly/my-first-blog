# Generated by Django 3.0.8 on 2020-08-11 11:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0061_auto_20200730_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='upload_data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]