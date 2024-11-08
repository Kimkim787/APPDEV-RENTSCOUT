from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, Group

from .managers import ScoutUserManager, LandlordCustomUserManager

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.core.validators import MinValueValidator


class AdminUser(AbstractBaseUser, PermissionsMixin):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 50, null=False, blank=False)
    email = models.EmailField(_("email address"), unique=True)
        
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ScoutUserManager()

        #define reverse accessor for GROUP
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        related_name="admin_user_groups"  # Specify a related_name to resolve the clash
    )
        #define reverse accessor for Permission
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="admin_user_permissions"  # Specify a related_name to resolve the clash
    )

class ScoutUser(AbstractBaseUser, PermissionsMixin):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDERS = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    userid = models.AutoField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    middlename = models.CharField(max_length = 20)
    birthdate = models.DateField(default = timezone.now)
    gender = models.CharField(max_length = 8, choices = GENDERS, default = MALE)
    barangay = models.CharField(max_length = 50, default = "", null=True)
    province = models.CharField(max_length = 50, default = "", null=True)
    city = models.CharField(max_length = 50, default = "", null=True)
    contact = models.CharField(max_length = 15, default="", null=True)
    
    def fullname(self):
        return f'{self.firstname} {self.lastname}'
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ScoutUserManager()

        #define reverse accessor for GROUP
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        related_name="scout_user_groups"  # Specify a related_name to resolve the clash
    )
        #define reverse accessor for Permission
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="scout_user_permissions"  # Specify a related_name to resolve the clash
    )


class ScoutUser_Landlord(AbstractBaseUser, PermissionsMixin):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDERS = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    userid = models.AutoField(primary_key=True)
    email = models.EmailField(_("email address"), unique=True)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    middlename = models.CharField(max_length = 20)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length = 8, choices = GENDERS, default = MALE)
    barangay = models.CharField(max_length = 50, default = "", null=True)
    province = models.CharField(max_length = 50, default = "", null=True)
    city = models.CharField(max_length = 50, default = "", null=True)
    contact = models.CharField(max_length = 15, default="", null=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = LandlordCustomUserManager()

        #define reverse accessor for GROUP
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        related_name="scout_landlord_groups"  # Specify a related_name to resolve the clash
    )
        #define reverse accessor for Permission
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="scout_landlord_permissions"  # Specify a related_name to resolve the clash
    )


    def __str__(self):
        return self.email

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    
class Building(models.Model):
    buildingid = models.AutoField(primary_key=True)
    building_owner = models.ForeignKey(ScoutUser_Landlord, on_delete = models.CASCADE, null=False, blank=False)
    building_name = models.CharField(max_length = 250, default="")
    zip_code = models.PositiveIntegerField(default=0, null=True, blank=True)
    street = models.CharField(max_length=75, blank=True, null=True)
    city = models.CharField(max_length=75, default="None")
    province = models.CharField(max_length=75, default="None")
    country = models.CharField(max_length=75, default="None")
    details = models.TextField(blank=True, null=True)
    rooms_vacant = models.IntegerField(validators = [MinValueValidator(0)])
    coordinates = models.CharField(max_length = 255, blank = False, null = False, default = "")
    building_image = models.FileField(upload_to = 'upload/building_imgs', blank = True, null = True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True, blank=True)

    def complete_address(self):
        return f"{self.zip_code}, {self.street}, {self.province}, {self.city}, {self.country}"

    class Meta:
        ordering = ['-average_rating']

class Policies(models.Model):
    policy_id = models.AutoField(primary_key=True)
    buildingid = models.ForeignKey(Building, on_delete = models.CASCADE)
    policy = models.TextField(default = "", null=True, blank = True)

    #   AMENITIES
class Highlights(models.Model):
    highlights_id = models.AutoField(primary_key=True)
    buildingid = models.ForeignKey(Building, on_delete = models.CASCADE)
    free_wifi = models.BooleanField(default=False)
    shared_kitchen = models.BooleanField(default=False)
    smoke_free = models.BooleanField(default=False)
    janitor = models.BooleanField(default=False)
    guard = models.BooleanField(default=False)
    waterbill = models.BooleanField(default=False)
    electricbill = models.BooleanField(default=False)
    food = models.BooleanField(default=False)

class Room(models.Model):
    roomid = models.AutoField(primary_key=True)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=250)
    person_free = models.IntegerField(validators = [ MinValueValidator(1)])
    current_male = models.IntegerField(default=0)
    current_female = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=100)
    # --------------FURNITURES------------------
    room_size = models.CharField(max_length = 20) # get l&w then concat
    shower = models.BooleanField(default=False)
    priv_bathroom = models.BooleanField(default=False)
    public_bathroom = models.BooleanField(default=False)
    AC = models.BooleanField(default=False) # aircon
    wardrobe = models.BooleanField(default = False)
    kitchen = models.BooleanField(default = False)
    bed = models.IntegerField(validators = [ MinValueValidator(0)])
    double_deck = models.IntegerField(validators = [ MinValueValidator(0)])
    free_wifi = models.BooleanField(default = False)

class Feedback(models.Model):
    ONE = "1"
    ONE_HALF = "1.5"
    TWO = "2"
    TWO_HALF = "2.5"
    THREE = "3"
    THREE_HALF = "3.5"
    FOUR = "4"
    FOUR_HALF = "4.5"
    FIVE = "5"
    ZERO = "0"
    RATING_CHOICES = [
        (ONE, '1'), (ONE_HALF, '1.5'),
        (TWO, '2'), (TWO_HALF, '2.5'),
        (THREE, '3'), (THREE_HALF, '3.5'),
        (FOUR, '4'), (FOUR_HALF, '4.5'),
        (FIVE, '5'), (ZERO, '0')
    ]
    feedbackid = models.AutoField(primary_key = True)
    boardingid = models.ForeignKey(Building, related_name = 'building_rating', on_delete = models.CASCADE)
    userid = models.ForeignKey(ScoutUser, related_name="reviewer", on_delete = models.CASCADE, default="", null=False, blank=False)
    rating = models.CharField(max_length = 10, choices = RATING_CHOICES, default = ZERO)
    message = models.TextField(default="")

@receiver([post_save, post_delete], sender=Feedback)
def update_building_rating(sender, instance, **kwargs):
    building = instance.boardingid
    avg_rating = building.building_rating.aggregate(Avg('rating'))['rating__avg'] or 0.0
    building.average_rating = round(avg_rating, 2)
    building.save()

class RoomImage(models.Model):
    room_imgID = models.AutoField(primary_key = True)
    room_img = models.FileField(upload_to = 'upload/room_imgs', blank = True, null = True)
    roomid = models.ForeignKey(Room, related_name = 'room_photo', on_delete = models.CASCADE, null = False, blank = False)


class ScoutUserBookmark(models.Model):
    buildingid = models.ForeignKey(Building, related_name="scoutuser_bookmark_building", on_delete=models.CASCADE)
    owner = models.ForeignKey(ScoutUser, related_name="scoutuser_bookmark_owner", on_delete=models.CASCADE)

class LandlordUserBookmark(models.Model):
    buildingid = models.ForeignKey(Building, related_name="landlord_bookmark_building", on_delete=models.CASCADE)
    owner = models.ForeignKey(ScoutUser_Landlord, related_name="landlord_bookmark_owner", on_delete=models.CASCADE)

class BuildingReport(models.Model):
    reportid = models.AutoField(primary_key=True)
    buildingid = models.ForeignKey(Building, related_name = 'building_reported', on_delete = models.CASCADE)
    reporter = models.ForeignKey(ScoutUser, related_name = 'reporting_user', on_delete = models.SET_NULL, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=250, null=False, blank=False, default="")

    class Meta:
        ordering = ['date_reported']

class Verification(models.Model):
    NOT_VERIFIED = 'Not Verified'
    PENDING = 'Pending'
    VERIFIED = 'Verified'
    status_choices = [
        (NOT_VERIFIED, 'Not Verified'),
        (PENDING, 'Pending'),
        (VERIFIED, 'Verified'),
    ]

    verificationid = models.AutoField(primary_key=True)
    buildingid = models.ForeignKey(Building, related_name = 'verify_building', on_delete = models.CASCADE)
    status = models.CharField(max_length = 15, choices = status_choices, default=NOT_VERIFIED)
    date_requested = models.DateTimeField(auto_now_add=True)

    # REASON FOR DENYING THE VERIFICATION
    deny_reason = models.TextField(null=True, blank=True)
