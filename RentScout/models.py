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
    profile_image = models.FileField(upload_to='upload/user_profiles', default = 'upload/user_profiles/user.png', null=True, blank=True)

    def fullname(self):
        return f'{self.firstname} {self.lastname}'
    
    @property
    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"

    usertype = models.CharField(max_length = 10, default="Boarder", null=False, blank=False)
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
    profile_image = models.FileField(upload_to='upload/user_profiles', default = 'upload/user_profiles/user.png', null=True, blank=True)

    usertype = models.CharField(max_length = 10, default="Landlord", null=False, blank=False)
    gcash = models.CharField(max_length = 15, default="", null=True, blank = True)
    
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

    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    @property
    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"
    
class Building(models.Model):
    buildingid = models.AutoField(primary_key=True)
    building_owner = models.ForeignKey(ScoutUser_Landlord, on_delete = models.CASCADE, null=False, blank=False)
    building_name = models.CharField(max_length = 250, default="")
    price = models.PositiveIntegerField(default=100)
    zip_code = models.PositiveIntegerField(default=0, null=True, blank=True)
    street = models.CharField(max_length=75, blank=True, null=True)
    city = models.CharField(max_length=75, default="None")
    province = models.CharField(max_length=75, default="None")
    country = models.CharField(max_length=75, default="None")
    details = models.TextField(blank=True, null=True)
    rooms_vacant = models.IntegerField(validators = [MinValueValidator(0)])
    coordinates = models.CharField(max_length = 255, blank = False, null = False, default = "")
    building_image = models.FileField(upload_to = 'upload/building_imgs', default='upload/building_imgs/no-image.png', blank = True, null = True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True, blank=True)
    gcash_qr = models.FileField(upload_to = 'upload/building_imgs/gcash', default='upload/building_imgs/gcash/no-image.png', blank = True, null = True)
    
    
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
    building_id = models.ForeignKey(Building, related_name = "room_of_building", on_delete=models.CASCADE)
    room_name = models.CharField(max_length=250)
    person_free = models.IntegerField(validators = [ MinValueValidator(0)])
    current_male = models.IntegerField(default=0)
    current_female = models.IntegerField(default=0)
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
    class Meta:
        ordering = ['buildingid__average_rating']
    
class BuildingReport(models.Model):
    reportid = models.AutoField(primary_key=True)
    buildingid = models.ForeignKey(Building, related_name = 'building_reported', on_delete = models.CASCADE)
    reporter = models.ForeignKey(ScoutUser, related_name = 'reporting_user', on_delete = models.SET_NULL, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=250, null=False, blank=False, default="")

    class Meta:
        ordering = ['buildingid__average_rating']

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

class Reservation(models.Model):
    ACCEPTED = 'Accepted'
    PENDING = 'Pending'
    DECLINED = 'Declined'
    PAYED = 'Payed'
    status_choices = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
        (PAYED, 'Payed')
    ]

    reservationid = models.AutoField(primary_key = True)
    roomid = models.ForeignKey(Room, related_name = 'reserved_room', on_delete = models.CASCADE) #, null = False, default=1
    userid = models.ForeignKey(ScoutUser, related_name = 'reservation_customer', on_delete=models.CASCADE, null = False)
    status = models.CharField(max_length = 10, choices = status_choices, default = PENDING, null = False, blank = False)
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created', '-last_updated']

class Certificate(models.Model):
    certificationid = models.AutoField(primary_key = True)
    buildingid = models.ForeignKey(Building, related_name = 'certification', on_delete = models.CASCADE)
    certificate_name = models.CharField(max_length = 100, null=False, blank=False, default="Certificate")
    image = models.FileField(upload_to = 'upload/building_imgs/certifications')
    date_uploaded = models.DateTimeField(auto_now_add = True)

class Message(models.Model):
    BOARDER = 'Boarder'
    LANDLORD = 'Landlord'
    sender_choices = [
        (LANDLORD, 'Landlord'),
        (BOARDER, 'Boarder')
    ]
    messageid = models.AutoField(primary_key = True)
    sender = models.CharField(max_length = 10, choices = sender_choices, null=False, blank=True, default="Boarder")
    message = models.TextField(blank=True, null=True, default="")
    image = models.FileField(upload_to = 'upload/message', blank = True, null = True)
    boarder = models.ForeignKey(ScoutUser, related_name = 'customer_message', on_delete=models.CASCADE)
    landlord = models.ForeignKey(ScoutUser_Landlord, related_name = 'landlord_message', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['date_created']

class BoarderNotification(models.Model):
    notificationid = models.AutoField(primary_key = True)
    buildingid = models.ForeignKey(Building, related_name='boarder_notify_content', on_delete = models.CASCADE)
    boarder = models.ForeignKey(ScoutUser, related_name = 'boarder_notify_recepient', on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add = True)
    status = models.BooleanField(default=False)

class LandlordNotification(models.Model):
    notificationid = models.AutoField(primary_key = True)
    buildingid = models.ForeignKey(Building, related_name='landlord_notify_content', on_delete = models.CASCADE)
    landlord = models.ForeignKey(ScoutUser_Landlord, related_name = 'landlord_notify_recepient', on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add = True)
    status = models.BooleanField(default=False)

class Payment(models.Model):
    ACCEPTED = 'Accepted'
    PENDING = 'Pending'
    DECLINED = 'Declined'
    HIDDEN = 'Hidden'
    payment_choices = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
        (HIDDEN, 'Hidden')
    ]

    paymentid = models.AutoField(primary_key = True)
    referralid = models.CharField(max_length = 60, blank=False, null=False, default="")
    payment_img = models.FileField(upload_to = 'upload/payments', blank=False, null=False, default='upload/payments/gcash_receipt.jpg')
    roomid = models.ForeignKey(Room, related_name = 'room_payed', on_delete = models.CASCADE)
    boarder = models.ForeignKey(ScoutUser, related_name = 'payment_sender', on_delete = models.CASCADE)
    status = models.CharField(max_length = 10, choices = payment_choices, default = PENDING)
    date_sent = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['date_sent']


class CreatedBoarder(models.Model):
    userid = models.PositiveIntegerField()
    email = models.CharField(max_length = 225)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    middlename = models.CharField(max_length = 20)
    birthdate = models.DateField(default = timezone.now)
    gender = models.CharField(max_length = 8)
    barangay = models.CharField(max_length = 50, default = "", null=True)
    province = models.CharField(max_length = 50, default = "", null=True)
    city = models.CharField(max_length = 50, default = "", null=True)
    contact = models.CharField(max_length = 15, default="", null=True)
    date_created = models.DateTimeField(auto_now = True)

    @property
    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    @property
    def get_address(self):
        return f'{self.barangay}, {self.province}, {self.city}'

class UpdatedBoarder(models.Model):
    userid = models.PositiveIntegerField()
    email = models.CharField(max_length = 225)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    middlename = models.CharField(max_length = 20)
    birthdate = models.DateField(default = timezone.now)
    gender = models.CharField(max_length = 8)
    barangay = models.CharField(max_length = 50, default = "", null=True)
    province = models.CharField(max_length = 50, default = "", null=True)
    city = models.CharField(max_length = 50, default = "", null=True)
    contact = models.CharField(max_length = 15, default="", null=True)
    date_created = models.DateTimeField(auto_now = True)

    @property
    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    @property
    def get_address(self):
        return f'{self.barangay}, {self.province}, {self.city}'

class CreatedLandlord(models.Model):
    userid = models.PositiveIntegerField()
    email = models.CharField(max_length = 225)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    middlename = models.CharField(max_length = 20)
    birthdate = models.DateField(default = timezone.now)
    gender = models.CharField(max_length = 8)
    barangay = models.CharField(max_length = 50, default = "", null=True)
    province = models.CharField(max_length = 50, default = "", null=True)
    city = models.CharField(max_length = 50, default = "", null=True)
    contact = models.CharField(max_length = 15, default="", null=True)
    date_created = models.DateTimeField(auto_now = True)

    @property
    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    @property
    def get_address(self):
        return f'{self.barangay}, {self.province}, {self.city}'

class UpdatedLandlord(models.Model):
    userid = models.PositiveIntegerField()
    email = models.CharField(max_length = 225)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    middlename = models.CharField(max_length = 20)
    birthdate = models.DateField(default = timezone.now, null=True, blank=True)
    gender = models.CharField(max_length = 8)
    barangay = models.CharField(max_length = 50, default = "", null=True)
    province = models.CharField(max_length = 50, default = "", null=True)
    city = models.CharField(max_length = 50, default = "", null=True)
    contact = models.CharField(max_length = 15, default="", null=True)
    date_created = models.DateTimeField(auto_now = True)

    @property
    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"
    
    @property
    def get_address(self):
        return f'{self.barangay}, {self.province}, {self.city}'

class CreatedBuilding(models.Model):
    buildingid = models.PositiveIntegerField()
    building_owner = models.CharField(max_length = 255, default="")
    building_name = models.CharField(max_length = 250, default="")
    price = models.PositiveIntegerField(default=100)
    zip_code = models.PositiveIntegerField(default=0, null=True, blank=True)
    street = models.CharField(max_length=75, blank=True, null=True)
    city = models.CharField(max_length=75, default="None")
    province = models.CharField(max_length=75, default="None")
    country = models.CharField(max_length=75, default="None")
    details = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length = 255, blank = False, null = False, default = "")
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

class UpdatedBuilding(models.Model):
    buildingid = models.PositiveIntegerField()
    building_owner = models.CharField(max_length = 255, default="")
    building_name = models.CharField(max_length = 250, default="")
    price = models.PositiveIntegerField(default=100)
    zip_code = models.PositiveIntegerField(default=0, null=True, blank=True)
    street = models.CharField(max_length=75, blank=True, null=True)
    city = models.CharField(max_length=75, default="None")
    province = models.CharField(max_length=75, default="None")
    country = models.CharField(max_length=75, default="None")
    details = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length = 255, blank = False, null = False, default = "")
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

class DeletedBuilding(models.Model):
    buildingid = models.PositiveIntegerField()
    building_owner = models.CharField(max_length = 255, default="")
    building_name = models.CharField(max_length = 250, default="")
    price = models.PositiveIntegerField(default=100)
    zip_code = models.PositiveIntegerField(default=0, null=True, blank=True)
    street = models.CharField(max_length=75, blank=True, null=True)
    city = models.CharField(max_length=75, default="None")
    province = models.CharField(max_length=75, default="None")
    country = models.CharField(max_length=75, default="None")
    details = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length = 255, blank = False, null = False, default = "")
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

class CreatedRoom(models.Model):
    roomid = models.PositiveIntegerField(default=1)
    owner = models.CharField(max_length = 250, default="")
    building_name = models.CharField(max_length = 250, default="")
    room_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now=True)

class UpdatedRoom(models.Model):
    roomid = models.PositiveIntegerField(default=1)
    owner = models.CharField(max_length = 250, default="")
    building_name = models.CharField(max_length = 250, default="")
    room_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now=True)

class DeletedRoom(models.Model):
    roomid = models.PositiveIntegerField(default=1)
    owner = models.CharField(max_length = 250, default="")
    building_name = models.CharField(max_length = 250, default="")
    room_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now=True)


class CreatedPayment(models.Model):
    paymentid = models.PositiveIntegerField()
    referralid = models.CharField(max_length = 60, default="")
    building_name = models.CharField(max_length = 250, default="")
    boarder_name = models.CharField(max_length = 250, default="")
    date_created = models.DateTimeField(auto_now=True)

class AcceptedPayment(models.Model):
    paymentid = models.PositiveIntegerField()
    referralid = models.CharField(max_length = 60, default="")
    building_name = models.CharField(max_length = 250, default="")
    boarder_name = models.CharField(max_length = 250, default="")
    date_created = models.DateTimeField(auto_now=True)

class DeniedPayment(models.Model):
    paymentid = models.PositiveIntegerField()
    referralid = models.CharField(max_length = 60, default="")
    building_name = models.CharField(max_length = 50, default="")
    boarder_name = models.CharField(max_length = 50, default="")
    date_created = models.DateTimeField(auto_now=True)

class CreatedReport(models.Model):
    reportid = models.PositiveIntegerField()
    building = models.CharField(max_length = 60, default="")
    reporter = models.CharField(max_length = 50, default="")
    reason = models.CharField(max_length = 255, default="")
    date_created = models.DateTimeField(auto_now=True)

class AcceptedReport(models.Model):
    reportid = models.PositiveIntegerField()
    building = models.CharField(max_length = 60, default="")
    reporter = models.CharField(max_length = 50, default="")
    reason = models.CharField(max_length = 255, default="")
    date_created = models.DateTimeField(auto_now=True)

class DeniedReport(models.Model):
    reportid = models.PositiveIntegerField()
    building = models.CharField(max_length = 60, default="")
    reporter = models.CharField(max_length = 50, default="")
    reason = models.CharField(max_length = 255, default="")
    date_created = models.DateTimeField(auto_now=True)



class CreatedVerification(models.Model):
    verificationid = models.PositiveIntegerField()
    building = models.CharField(max_length = 60, default="")
    date_created = models.DateTimeField(auto_now=True)

class AcceptedVerification(models.Model):
    verificationid = models.PositiveIntegerField()
    building = models.CharField(max_length = 60, default="")
    date_created = models.DateTimeField(auto_now=True)

class DeniedVerification(models.Model):
    verificationid = models.PositiveIntegerField()
    building = models.CharField(max_length = 60, default="")
    date_created = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length = 255, default="")

class DeletedVerification(models.Model):
    verificationid = models.PositiveIntegerField()
    building = models.CharField(max_length = 60, default="")
    date_created = models.DateTimeField(auto_now=True)

