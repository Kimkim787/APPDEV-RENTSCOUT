# Generated by Django 4.2.4 on 2024-09-27 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomimage',
            name='room_img',
            field=models.FileField(blank=True, null=True, upload_to='upload/room_imgs'),
        ),
    ]
