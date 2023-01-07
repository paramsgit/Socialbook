from django.contrib import admin
from .models import Profile,Post,Likepost,followers,Images,cmessage,messageroom,saveotp
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Likepost)
admin.site.register(saveotp)
admin.site.register(followers)
admin.site.register(Images)
admin.site.register(cmessage)
admin.site.register(messageroom)
