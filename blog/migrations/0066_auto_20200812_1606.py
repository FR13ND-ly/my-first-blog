# Generated by Django 3.0.8 on 2020-08-12 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0065_auto_20200811_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='blog.Tag'),
        ),
    ]