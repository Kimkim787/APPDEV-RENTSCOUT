# Generated by Django 4.2.4 on 2024-11-05 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0002_alter_building_average_rating_buildingreports'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BuildingReports',
            new_name='BuildingReport',
        ),
        migrations.AlterModelOptions(
            name='buildingreport',
            options={'ordering': ['date_reported']},
        ),
    ]
