# Generated by Django 4.2.4 on 2024-09-17 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomImages',
            fields=[
                ('room_imgID', models.AutoField(primary_key=True, serialize=False)),
                ('room_img', models.FileField(blank=True, null=True, upload_to='room_imgs')),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentScout.room')),
            ],
        ),
        migrations.CreateModel(
            name='BuildingImages',
            fields=[
                ('building_imgID', models.AutoField(primary_key=True, serialize=False)),
                ('building_img', models.FileField(blank=True, null=True, upload_to='building_imgs')),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentScout.building')),
            ],
        ),
    ]
