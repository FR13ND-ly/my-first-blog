# Generated by Django 3.0.1 on 2020-03-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0053_ad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
