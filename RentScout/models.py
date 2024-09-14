from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.  
class User(models.Model):
    userid = models.AutoField(primary_key=True)
    user_acc = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    middlename = models.CharField(max_length = 20)
    birthdate = models.DateField(default = timezone.now)

class Building(models.Model):
    buildingid = models.AutoField(primary_key=True)
    zip_code = models.PositiveIntegerField(default=0, null=True, blank=True)
    street = models.CharField(max_length=75, blank=True, null=True)
    city = models.CharField(max_length=75, default="None")
    province = models.CharField(max_length=75, default="None")
    country = models.CharField(max_length=75, default="None")
    details = models.TextField(blank=True, null=True)
    rooms_vacant = models.IntegerChoices(default=1)

class Policies(models.Model):
    policy_id = models.AutoField(primary_key=True)
    buildingid = models.ForeignKey(Building, on_delete = models.CASCADE)
    policy = models.TextField(default = "", null=True, blank = True)

class Facilities(models.Model):
    facil_id = models.AutoField(primary_key=True)
    buildingid = models.ForeignKey(Building, on_delete = models.CASCADE)
    free_wifi = models.BooleanField(default=False)
    shared_kitchen = models.BooleanField(default=False)
    smoke_free = models.BooleanField(default=False)
    janitor = models.BooleanField(default=False)
    waterbill = models.BooleanField(default=False)
    electricbill = models.BooleanField(default=False)
    comfort_room = models.BooleanField(default = False)
    food = models.BooleanField(default=False)

class Room(models.Model):
    buildingid = models.AutoField(primary_key=True)
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, default="", blank=False, null=False)
    room_name = models.CharField(max_length=250)
    person_free = models.IntegerChoices(default=1)
    current_male = models.IntegerField(default=0)
    current_female = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=100)
    # --------------FURNITURES------------------
    room_size = models.CharField(max_length = 20) # get l&w then concat
    shower = models.BooleanField(default=False)
    priv_bathrooom = models.BooleanField(default=False)
    public_bathroom = models.BooleanField(default=False)
    AC = models.BooleanField(default=False) # aircon
    wardrobe = models.BooleanField(default = False)
    kitchen = models.BooleanField(default = False)
    bedroom = models.IntegerChoices(default=0)
    double_deck = models.IntegerChoices(default=0)
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
    baordingid = models.ForeignKey(Building, on_delete = models.CASCADE)
    rating = models.IntegerChoices(choices = RATING_CHOICES, default = ZERO)
    message = models.TextField(default="")



