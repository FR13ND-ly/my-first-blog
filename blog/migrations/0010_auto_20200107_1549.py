# Generated by Django 3.0.1 on 2020-01-07 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200107_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='blog/static/media/'),
        ),
    ]
