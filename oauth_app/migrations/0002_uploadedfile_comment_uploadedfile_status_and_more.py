# Generated by Django 4.2.11 on 2024-03-29 21:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='comment',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='status',
            field=models.CharField(default='Not Completed', max_length=20),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
