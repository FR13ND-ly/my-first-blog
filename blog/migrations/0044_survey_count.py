# Generated by Django 3.0.1 on 2020-02-08 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0043_post_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
