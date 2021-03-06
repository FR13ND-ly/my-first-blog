# Generated by Django 3.0.1 on 2020-02-04 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0032_auto_20200204_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='Radiovariants',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('survey_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Survey')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('blog.survey', models.Model),
        ),
    ]
