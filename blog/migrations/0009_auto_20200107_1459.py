# Generated by Django 3.0.1 on 2020-01-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_cover_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, default="'/media/blog/static/media/great-4.jpg'", null=True, upload_to='blog/static/media/'),
        ),
    ]
