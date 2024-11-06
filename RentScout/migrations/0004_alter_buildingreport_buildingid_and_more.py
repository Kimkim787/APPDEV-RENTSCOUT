# Generated by Django 4.2.4 on 2024-11-06 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0003_rename_buildingreports_buildingreport_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingreport',
            name='buildingid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='building_reported', to='RentScout.building'),
        ),
        migrations.AlterField(
            model_name='buildingreport',
            name='reporter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporting_user', to='RentScout.scoutuser'),
        ),
    ]
