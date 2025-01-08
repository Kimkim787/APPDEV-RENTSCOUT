# Generated by Django 4.2.4 on 2025-01-07 02:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('buildingid', models.AutoField(primary_key=True, serialize=False)),
                ('building_name', models.CharField(default='', max_length=250)),
                ('price', models.PositiveIntegerField(default=100)),
                ('zip_code', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('street', models.CharField(blank=True, max_length=75, null=True)),
                ('city', models.CharField(default='None', max_length=75)),
                ('province', models.CharField(default='None', max_length=75)),
                ('country', models.CharField(default='None', max_length=75)),
                ('details', models.TextField(blank=True, null=True)),
                ('rooms_vacant', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('coordinates', models.CharField(default='', max_length=255)),
                ('building_image', models.FileField(blank=True, null=True, upload_to='upload/building_imgs')),
                ('average_rating', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True)),
                ('gcash_qr', models.FileField(blank=True, null=True, upload_to='upload/building_imgs/gcash')),
            ],
            options={
                'ordering': ['-average_rating'],
            },
        ),
        migrations.CreateModel(
            name='CreatedBoarder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.PositiveIntegerField()),
                ('email', models.CharField(max_length=225)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('middlename', models.CharField(max_length=20)),
                ('birthdate', models.DateField(default=django.utils.timezone.now)),
                ('gender', models.CharField(max_length=8)),
                ('barangay', models.CharField(default='', max_length=50, null=True)),
                ('province', models.CharField(default='', max_length=50, null=True)),
                ('city', models.CharField(default='', max_length=50, null=True)),
                ('contact', models.CharField(default='', max_length=15, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreatedBuilding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buildingid', models.PositiveIntegerField()),
                ('building_owner', models.CharField(default='', max_length=255)),
                ('building_name', models.CharField(default='', max_length=250)),
                ('price', models.PositiveIntegerField(default=100)),
                ('zip_code', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('street', models.CharField(blank=True, max_length=75, null=True)),
                ('city', models.CharField(default='None', max_length=75)),
                ('province', models.CharField(default='None', max_length=75)),
                ('country', models.CharField(default='None', max_length=75)),
                ('details', models.TextField(blank=True, null=True)),
                ('coordinates', models.CharField(default='', max_length=255)),
                ('average_rating', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreatedLandlord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.PositiveIntegerField()),
                ('email', models.CharField(max_length=225)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('middlename', models.CharField(max_length=20)),
                ('birthdate', models.DateField(default=django.utils.timezone.now)),
                ('gender', models.CharField(max_length=8)),
                ('barangay', models.CharField(default='', max_length=50, null=True)),
                ('province', models.CharField(default='', max_length=50, null=True)),
                ('city', models.CharField(default='', max_length=50, null=True)),
                ('contact', models.CharField(default='', max_length=15, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreatedRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomid', models.PositiveIntegerField(default=1)),
                ('owner', models.CharField(default='', max_length=250)),
                ('building_name', models.CharField(default='', max_length=250)),
                ('room_name', models.CharField(max_length=250)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedBuilding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buildingid', models.PositiveIntegerField()),
                ('building_owner', models.CharField(default='', max_length=255)),
                ('building_name', models.CharField(default='', max_length=250)),
                ('price', models.PositiveIntegerField(default=100)),
                ('zip_code', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('street', models.CharField(blank=True, max_length=75, null=True)),
                ('city', models.CharField(default='None', max_length=75)),
                ('province', models.CharField(default='None', max_length=75)),
                ('country', models.CharField(default='None', max_length=75)),
                ('details', models.TextField(blank=True, null=True)),
                ('coordinates', models.CharField(default='', max_length=255)),
                ('average_rating', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeletedRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomid', models.PositiveIntegerField(default=1)),
                ('owner', models.CharField(default='', max_length=250)),
                ('building_name', models.CharField(default='', max_length=250)),
                ('room_name', models.CharField(max_length=250)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('roomid', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=250)),
                ('person_free', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('current_male', models.IntegerField(default=0)),
                ('current_female', models.IntegerField(default=0)),
                ('room_size', models.CharField(max_length=20)),
                ('shower', models.BooleanField(default=False)),
                ('priv_bathroom', models.BooleanField(default=False)),
                ('public_bathroom', models.BooleanField(default=False)),
                ('AC', models.BooleanField(default=False)),
                ('wardrobe', models.BooleanField(default=False)),
                ('kitchen', models.BooleanField(default=False)),
                ('bed', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('double_deck', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('free_wifi', models.BooleanField(default=False)),
                ('building_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_of_building', to='RentScout.building')),
            ],
        ),
        migrations.CreateModel(
            name='ScoutUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('middlename', models.CharField(max_length=20)),
                ('birthdate', models.DateField(default=django.utils.timezone.now)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=8)),
                ('barangay', models.CharField(default='', max_length=50, null=True)),
                ('province', models.CharField(default='', max_length=50, null=True)),
                ('city', models.CharField(default='', max_length=50, null=True)),
                ('contact', models.CharField(default='', max_length=15, null=True)),
                ('profile_image', models.FileField(blank=True, default='upload/user_profiles/user.png', null=True, upload_to='upload/user_profiles')),
                ('usertype', models.CharField(default='Boarder', max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, related_name='scout_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='scout_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UpdatedBoarder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.PositiveIntegerField()),
                ('email', models.CharField(max_length=225)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('middlename', models.CharField(max_length=20)),
                ('birthdate', models.DateField(default=django.utils.timezone.now)),
                ('gender', models.CharField(max_length=8)),
                ('barangay', models.CharField(default='', max_length=50, null=True)),
                ('province', models.CharField(default='', max_length=50, null=True)),
                ('city', models.CharField(default='', max_length=50, null=True)),
                ('contact', models.CharField(default='', max_length=15, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UpdatedBuilding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buildingid', models.PositiveIntegerField()),
                ('building_owner', models.CharField(default='', max_length=255)),
                ('building_name', models.CharField(default='', max_length=250)),
                ('price', models.PositiveIntegerField(default=100)),
                ('zip_code', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('street', models.CharField(blank=True, max_length=75, null=True)),
                ('city', models.CharField(default='None', max_length=75)),
                ('province', models.CharField(default='None', max_length=75)),
                ('country', models.CharField(default='None', max_length=75)),
                ('details', models.TextField(blank=True, null=True)),
                ('coordinates', models.CharField(default='', max_length=255)),
                ('average_rating', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UpdatedLandlord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.PositiveIntegerField()),
                ('email', models.CharField(max_length=225)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('middlename', models.CharField(max_length=20)),
                ('birthdate', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('gender', models.CharField(max_length=8)),
                ('barangay', models.CharField(default='', max_length=50, null=True)),
                ('province', models.CharField(default='', max_length=50, null=True)),
                ('city', models.CharField(default='', max_length=50, null=True)),
                ('contact', models.CharField(default='', max_length=15, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UpdatedRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomid', models.PositiveIntegerField(default=1)),
                ('owner', models.CharField(default='', max_length=250)),
                ('building_name', models.CharField(default='', max_length=250)),
                ('room_name', models.CharField(max_length=250)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, related_name='admin_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='admin_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('verificationid', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Not Verified', 'Not Verified'), ('Pending', 'Pending'), ('Verified', 'Verified')], default='Not Verified', max_length=15)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('deny_reason', models.TextField(blank=True, null=True)),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verify_building', to='RentScout.building')),
            ],
        ),
        migrations.CreateModel(
            name='ScoutUserBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoutuser_bookmark_building', to='RentScout.building')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoutuser_bookmark_owner', to='RentScout.scoutuser')),
            ],
        ),
        migrations.CreateModel(
            name='ScoutUser_Landlord',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('middlename', models.CharField(max_length=20)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=8)),
                ('barangay', models.CharField(default='', max_length=50, null=True)),
                ('province', models.CharField(default='', max_length=50, null=True)),
                ('city', models.CharField(default='', max_length=50, null=True)),
                ('contact', models.CharField(default='', max_length=15, null=True)),
                ('profile_image', models.FileField(blank=True, default='upload/user_profiles/user.png', null=True, upload_to='upload/user_profiles')),
                ('usertype', models.CharField(default='Landlord', max_length=10)),
                ('gcash', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, related_name='scout_landlord_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='scout_landlord_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('room_imgID', models.AutoField(primary_key=True, serialize=False)),
                ('room_img', models.FileField(blank=True, null=True, upload_to='upload/room_imgs')),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_photo', to='RentScout.room')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservationid', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Payed', 'Payed')], default='Pending', max_length=10)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserved_room', to='RentScout.room')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_customer', to='RentScout.scoutuser')),
            ],
            options={
                'ordering': ['-created', '-last_updated'],
            },
        ),
        migrations.CreateModel(
            name='Policies',
            fields=[
                ('policy_id', models.AutoField(primary_key=True, serialize=False)),
                ('policy', models.TextField(blank=True, default='', null=True)),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentScout.building')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentid', models.AutoField(primary_key=True, serialize=False)),
                ('referralid', models.CharField(default='', max_length=60)),
                ('payment_img', models.FileField(default='upload/payments/gcash_receipt.jpg', upload_to='upload/payments')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Hidden', 'Hidden')], default='Pending', max_length=10)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('boarder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_sender', to='RentScout.scoutuser')),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_payed', to='RentScout.room')),
            ],
            options={
                'ordering': ['date_sent'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messageid', models.AutoField(primary_key=True, serialize=False)),
                ('sender', models.CharField(blank=True, choices=[('Landlord', 'Landlord'), ('Boarder', 'Boarder')], default='Boarder', max_length=10)),
                ('message', models.TextField(blank=True, default='', null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='upload/message')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('boarder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_message', to='RentScout.scoutuser')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_message', to='RentScout.scoutuser_landlord')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='LandlordUserBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_bookmark_building', to='RentScout.building')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_bookmark_owner', to='RentScout.scoutuser_landlord')),
            ],
            options={
                'ordering': ['buildingid__average_rating'],
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
            name='Highlights',
            fields=[
                ('highlights_id', models.AutoField(primary_key=True, serialize=False)),
                ('free_wifi', models.BooleanField(default=False)),
                ('shared_kitchen', models.BooleanField(default=False)),
                ('smoke_free', models.BooleanField(default=False)),
                ('janitor', models.BooleanField(default=False)),
                ('guard', models.BooleanField(default=False)),
                ('waterbill', models.BooleanField(default=False)),
                ('electricbill', models.BooleanField(default=False)),
                ('food', models.BooleanField(default=False)),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentScout.building')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedbackid', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.CharField(choices=[('1', '1'), ('1.5', '1.5'), ('2', '2'), ('2.5', '2.5'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5'), ('0', '0')], default='0', max_length=10)),
                ('message', models.TextField(default='')),
                ('boardingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='building_rating', to='RentScout.building')),
                ('userid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to='RentScout.scoutuser')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('certificationid', models.AutoField(primary_key=True, serialize=False)),
                ('certificate_name', models.CharField(default='Certificate', max_length=100)),
                ('image', models.FileField(upload_to='upload/building_imgs/certifications')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certification', to='RentScout.building')),
            ],
        ),
        migrations.CreateModel(
            name='BuildingReport',
            fields=[
                ('reportid', models.AutoField(primary_key=True, serialize=False)),
                ('date_reported', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(default='', max_length=250)),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='building_reported', to='RentScout.building')),
                ('reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporting_user', to='RentScout.scoutuser')),
            ],
            options={
                'ordering': ['buildingid__average_rating'],
            },
        ),
        migrations.AddField(
            model_name='building',
            name='building_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentScout.scoutuser_landlord'),
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
