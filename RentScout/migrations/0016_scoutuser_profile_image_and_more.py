# Generated by Django 4.2.4 on 2024-12-21 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RentScout', '0015_building_gcash_qr_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoutuser',
            name='profile_image',
            field=models.FileField(blank=True, default='user.png', null=True, upload_to='upload/user_profiles'),
        ),
        migrations.AddField(
            model_name='scoutuser_landlord',
            name='profile_image',
            field=models.FileField(blank=True, default='user.png', null=True, upload_to='upload/user_profiles'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messageid', models.AutoField(primary_key=True, serialize=False)),
                ('sender', models.CharField(blank=True, choices=[('Landlord', 'Landlord'), ('Boarder', 'Boarder')], default='Boarder', max_length=10)),
                ('message', models.TextField(default='')),
                ('image', models.FileField(upload_to='upload/message')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('border', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_message', to='RentScout.scoutuser')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_message', to='RentScout.scoutuser_landlord')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='LandlordNotification',
            fields=[
                ('notificationid', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_notify_content', to='RentScout.building')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_notify_recepient', to='RentScout.scoutuser_landlord')),
            ],
        ),
        migrations.CreateModel(
            name='BoarderNotification',
            fields=[
                ('notificationid', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('boarder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boarder_notify_recepient', to='RentScout.scoutuser')),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boarder_notify_content', to='RentScout.building')),
            ],
        ),
    ]
