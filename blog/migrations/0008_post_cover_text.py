# Generated by Django 3.0.1 on 2020-01-06 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200106_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover_text',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
