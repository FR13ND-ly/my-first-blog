# Generated by Django 3.0.1 on 2020-02-05 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0037_auto_20200205_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeofvote', models.BooleanField(default=False)),
                ('variant', models.CharField(max_length=200)),
                ('question', models.CharField(max_length=200)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey', to='blog.Post')),
            ],
        ),
        migrations.AlterField(
            model_name='vote',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote', to='blog.Survey'),
        ),
        migrations.DeleteModel(
            name='Variant',
        ),
    ]
