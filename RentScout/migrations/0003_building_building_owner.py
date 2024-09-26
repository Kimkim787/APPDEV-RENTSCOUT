# Generated by Django 4.2.4 on 2024-09-17 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0002_roomimages_buildingimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='building_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]