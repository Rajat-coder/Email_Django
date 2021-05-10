from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_countries.fields import CountryField

# Create your models here.

class GENDER(object):
    MALE=1
    FEMALE=2
    OTHER=3

class User(AbstractUser):
    GENDER_TYPE=(
        (GENDER.MALE,"Male"),
        (GENDER.FEMALE,"Female"),
        (GENDER.OTHER,"Other")
    )
    gender_type=models.PositiveIntegerField(choices=GENDER_TYPE,default=GENDER.MALE)
    mobile=models.CharField(max_length=15,null=True,blank=True)
    otp_code=models.CharField(max_length=255,null=True,blank=True)
    otp_created_at=models.DateTimeField(default=timezone.now)
    country=CountryField(null=True,blank=True)
    profile_image=models.ImageField(upload_to="profile_image",default='profile_image/default_image.png')







