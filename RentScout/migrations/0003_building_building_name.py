# Generated by Django 4.2.4 on 2024-09-15 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0002_rename_baordingid_feedback_boardingid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='building_name',
            field=models.CharField(default='', max_length=250),
        ),
    ]
