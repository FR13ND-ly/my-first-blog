# Generated by Django 3.0.1 on 2020-02-18 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0050_remove_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='blog/static/media/'),
        ),
    ]
