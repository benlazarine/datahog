# Generated by Django 2.1.1 on 2019-01-07 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesummary',
            name='size_timeline_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filesummary',
            name='type_chart_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
