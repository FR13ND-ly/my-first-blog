# Generated by Django 3.0.1 on 2020-01-29 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_likes_count'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
