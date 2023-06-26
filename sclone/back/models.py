from ast import Pass
from distutils.command.upload import upload
from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from io import BytesIO
# from pil import Im
# imp
from django.core.files import File

from datetime import date, datetime

User=get_user_model()
# Create your models here.

class Profile(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    mail_verification=models.BooleanField(default=True)
    id_user= models.IntegerField()
    bio= models.TextField()
    location= models.CharField(max_length=100,blank=True,default="Unknown")
    role= models.CharField(max_length=100,blank=True,default="Can't say")
    fname= models.CharField(max_length=100,default="Mr./Mrs.")
    lname= models.CharField(max_length=100,default="Unknown",)
    status= models.CharField(max_length=100,default="Unknown",)
    file = models.ImageField(upload_to='images',default='default/defaultprofile.jpg')
    cover = models.ImageField(upload_to='coverimages',default='default/blank.png')
    joining=models.DateField(default=date.today)
    dob=models.DateField(default=date.today)


    
    def __str__(self) :
        return self.user.username
    
    
    

class Images(models.Model):
    # user= models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    file = models.ImageField(upload_to='images')
    # text = models.CharField(max_length=100,default='h')
    # uploaded = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.user.username
    
# def compress(image):
#     im = Image.open(image)
#     # create a BytesIO object
#     im_io = BytesIO() 
#     # save image to BytesIO object
#     im.save(im_io, 'JPEG', quality=70) 
#     # create a django-friendly Files object
#     new_image = File(im_io, name=image.name)
#     return new_image

class Post(models.Model):
    # profilephoto=models.ForeignKey(Profile,related_name='posts',on_delete=models.CASCADE)
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField(upload_to='posts')
    caption=models.TextField()
    tam=models.DateTimeField(default=datetime.now)
    likes=models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
    
    


class Likepost(models.Model):
    postid=models.CharField(max_length=500)
    username=models.CharField(max_length=100)

    def __str__(self):
        return self.username

class followers(models.Model):
    follower=models.CharField(max_length=100)
    user=models.CharField(max_length=100)

    def __str__(self):
        return self.user

class room(models.Model):
    roomname=models.CharField(max_length=100,default='room')
    roomid=models.IntegerField()
    
    def __str__(self):
        return self.roomid

class cmessage(models.Model):
    value=models.CharField(max_length=1000000)
    samya=models.DateTimeField(default=datetime.now)
    room=models.CharField(max_length=1000,blank=True)
    sender=models.CharField(max_length=10000,blank=True)

    def __str__(self):
        return self.room

class messageroom(models.Model):
    sender=models.CharField(max_length=1000)
    reci=models.CharField(max_length=1000)
    messageroomid=models.UUIDField(primary_key=True,default=uuid.uuid4)
    lastmessage=models.DateTimeField(default=datetime.now)

class saveotp(models.Model):
    email=models.CharField(max_length=30)
    when=models.DateTimeField(default=datetime.now)
    otp=models.CharField(max_length=8)

    def __str__(self):
        return self.email
    

    




