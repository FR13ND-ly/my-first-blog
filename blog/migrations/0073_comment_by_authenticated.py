# Generated by Django 3.0.8 on 2020-08-15 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0072_comment_by_administration'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='by_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
