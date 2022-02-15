from django.db import models
from django.core import validators
from django.contrib.auth.models import User


class Profiles(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    profile_pic = models.FileField(upload_to='static/profiles', default='static/images/sample_user.jpg')
    created_date = models.DateTimeField(auto_now_add=True)

class UserOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.SmallIntegerField()




class Contact(models.Model):
    firstname= models.CharField(max_length=50,null=True,validators=[validators.MinLengthValidator(2)])
    lastname=models.CharField(max_length=50, null=True, validators=[validators.MinLengthValidator(2)])
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message=models.TextField()
    def __str__(self):
        return self.firstname
