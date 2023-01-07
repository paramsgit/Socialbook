from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name="index"),
    path('signup', views.signup,name="signup"),
    path('upload', views.upload,name="upload"),
    path('crop', views.crop,name="crop"),
    path('verification', views.forgotpass,name="verification"),
    path('maik', views.maik,name="maik"),
    path('mail_verification', views.signup_verification,name="signup_verification"),
    path('changepass', views.changepass,name="changepass"),
    path('verify_otp', views.verify_otp,name="verify_otp"),
    path('sendm', views.sendm,name="sendm"),
    path('chatsearch', views.searchchat,name="chatsearch"),
    path('getm/<str:rr>/', views.getm,name="getm"),
    path('chat', views.chat,name="chat"),
    path('deletepost', views.deletepost,name="deletepost"),
    path('followsme', views.followsme,name="followsme"),
    path('youfollows', views.youfollows,name="youfollows"),
    path('cover', views.cover,name="cover"),
    path('temp', views.tempp,name="temp"),
    path('search', views.search,name="search"),
    path('follow', views.follow,name="follow"),
    path('profile/<str:pk>', views.profile,name="profile"),
    path('chatroom/<str:pk>', views.chatroom,name="chatroom"),
    path('like_post', views.like_post,name="like_post"),
    path('signin', views.signin,name="signin"),
    path('signout', views.signout,name="signout"),
    path('psettings', views.psettings,name="psettings"),
    

]