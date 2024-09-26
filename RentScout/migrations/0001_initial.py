# Generated by Django 4.2.4 on 2024-09-24 14:49

from django.conf import settings
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
                ('zip_code', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('street', models.CharField(blank=True, max_length=75, null=True)),
                ('city', models.CharField(default='None', max_length=75)),
                ('province', models.CharField(default='None', max_length=75)),
                ('country', models.CharField(default='None', max_length=75)),
                ('details', models.TextField(blank=True, null=True)),
                ('rooms_vacant', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('roomid', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=250)),
                ('person_free', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('current_male', models.IntegerField(default=0)),
                ('current_female', models.IntegerField(default=0)),
                ('price', models.PositiveIntegerField(default=100)),
                ('room_size', models.CharField(max_length=20)),
                ('shower', models.BooleanField(default=False)),
                ('priv_bathrooom', models.BooleanField(default=False)),
                ('public_bathroom', models.BooleanField(default=False)),
                ('AC', models.BooleanField(default=False)),
                ('wardrobe', models.BooleanField(default=False)),
                ('kitchen', models.BooleanField(default=False)),
                ('bed', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('double_deck', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('free_wifi', models.BooleanField(default=False)),
                ('building_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='RentScout.building')),
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
            name='RoomImage',
            fields=[
                ('room_imgID', models.AutoField(primary_key=True, serialize=False)),
                ('room_img', models.FileField(blank=True, null=True, upload_to='room_imgs')),
                ('roomid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_photo', to='RentScout.room')),
            ],
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
                ('boardingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentScout.building')),
            ],
        ),
        migrations.CreateModel(
            name='BuildingImage',
            fields=[
                ('building_imgID', models.AutoField(primary_key=True, serialize=False)),
                ('building_img', models.FileField(blank=True, null=True, upload_to='building_imgs')),
                ('buildingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='building_photo', to='RentScout.building')),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='building_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
