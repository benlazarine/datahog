# Generated by Django 2.1.1 on 2018-10-12 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatelog',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y%m%d%H%M%S/'),
        ),
    ]
