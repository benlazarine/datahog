# Generated by Django 2.1.1 on 2019-03-22 22:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('file_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importeddirectory',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
