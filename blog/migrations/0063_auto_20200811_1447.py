# Generated by Django 3.0.8 on 2020-08-11 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0062_image_upload_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='upload_data',
            new_name='upload_date',
        ),
    ]