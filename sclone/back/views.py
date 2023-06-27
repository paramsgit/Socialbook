from cProfile import Profile
from email.mime import image, message
from http.client import HTTPResponse
from imaplib import _Authenticator
import imp
from itertools import chain
import json,requests
from random import randint
from operator import contains
import random
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.utils.html import strip_tags
from django.conf import settings

from io import BytesIO
from django.core.files import File
from django.http import JsonResponse

from .forms import ImageForm,liker

from .models import Likepost, Profile,Post, followers,messageroom,cmessage,saveotp
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def index(request):
    form = liker(request.POST or None,request.FILES or None)
    user_obj=User.objects.get(username=request.user.username)
    
    user_profile=Profile.objects.get(user=user_obj)
    if user_profile.mail_verification == False:
        return redirect('/mail_verification') 
    # profile_photo=Image.objects.get(user=user_obj)
    posts=Post.objects.all().order_by('tam')
    postlist=[]
    posts22=Post.objects.filter(user=request.user.username)
    noofposts=len(posts22)
    user_followers2=len(followers.objects.filter(user=request.user.username))
    user_following2=len(followers.objects.filter(follower=request.user.username))
    
    
    userfollowinglist=[]
    feed=[]
    

    userf=followers.objects.filter(follower=request.user.username)
    
    userfpdata=[]
    for u in userf:
        userfollowinglist.append(u.user)
        fl=Post.objects.filter(user=u.user)
        feed.append(fl)
    
    # newfeed
    newfeed=[]
    newfollowlist=userfollowinglist
    newfollowlist.append(request.user.username)
    
    # print(newfollowlist)
    for po in posts:
        if po.user in newfollowlist:
            # print(po.user)
            newfeed.append(po)
            
    
    
    feedlist=list(chain(*feed))
    
    
    

    #  user sugg
    alll=User.objects.all()
    user_following_all = []
    for user in userf:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    new_suggestions_list = [x for x in list(alll) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        # print(users.id)
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    lsugg = list(chain(*username_profile_list))
    
    
    userfpdata.append("")
    for k in userf:
        uuu=User.objects.get(username=k.user)
        
        ppp=Profile.objects.get(id_user=uuu.id)
        userfpdata.append(ppp)

    uuu=User.objects.get(username=request.user)
        
    ppp=Profile.objects.get(id_user=uuu.id)
    userfpdata.append(ppp)
    
    

    # postuserdata=list(chain(*userfpdata))
    # print(userfpdata)     
    #    
    # allliked posts
    likedposts=Likepost.objects.filter(username=request.user)
    likedpostsid=[]
    for i in likedposts:
        likedpostsid.append(i.postid)
    
    # nasa Image
    response_code=400
    # try:
    #     request_api=requests.get('https://api.nasa.gov/planetary/apod?api_key=gOEFbB7Td1cAtnFgsOrRbuF440Pc9aXAR9KcDfBg')
    #     # print(request_api)
    #     response_code=request_api.status_code
    #     print(type(response_code))
    #     data = request_api.text
    #     parse_json=json.loads(data)
    #     print(parse_json['copyright'])
    # except Exception as e:
    #     print(e)
    
    
    return render(request,'home.html',{'user_profile':user_profile,'posts':newfeed,'lsugg':lsugg[:4],'form':form,'postuserdata':userfpdata,'user_following':user_following2,'user_followers':user_followers2,'noofposts':noofposts,'likedpostsid':likedpostsid})
 
def signup(request): 
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password2=request.POST['cpassword']
        
      
        
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email already registred')
            return redirect('signup')   
        elif User.objects.filter(username=username).exists():
            messages.info(request,'Username already registred')
            return redirect('signup') 
        elif password!=password2:
            messages.info(request,'Passwords are not matching')
            return redirect('signup') 
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            
            # login redirect to settings
            user_login=auth.authenticate(username=username,password=password)
            auth.login(request,user_login)
            # profile

            user_model=User.objects.get(username=username)
            new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
            new_profile.mail_verification=False
            new_profile.save()
            return redirect('/mail_verification') 

    return render(request,'signup.html')  

@login_required(login_url='signin')
def signup_verification(request):
    emaill=request.user.email
    print(emaill)
    if request.method=='POST':
        emaill=request.POST['emaill']
        otp_filled=request.POST['otp']
        user_otp=saveotp.objects.filter(email=emaill)
        if(user_otp[0].otp==otp_filled):
            print("Matched")
            user_obj=User.objects.get(email=emaill)
            usp=Profile.objects.get(user=user_obj)
            usp.mail_verification=True
            usp.save()
            return JsonResponse({'otpsend':True,'respons':'OTP is matched'})
            
        else:
            print("Not Matching")
            
            return JsonResponse({'otpsend':False,'respons':'OTP is not matching'})
    return render(request,'signup_verify.html',{'mail':emaill})
   

@login_required(login_url='signin')
def like_post(request):
    form = liker(request.POST or None,request.FILES or None)
    
    if form.is_valid():
        # form.save()
        postid=form.cleaned_data['postid']
        username=form.cleaned_data['username']
        print(username,postid)
        # return redirect('/')
    # username=request.user.username
    # postid=request.GET.get('postid')
    
    post=Post.objects.get(id=postid)

    likefilter=Likepost.objects.filter(postid=postid,username=username).first()

    if likefilter is None:
        newlike=Likepost.objects.create(postid=postid,username=username)
        newlike.save()

        post.likes=post.likes+1
        post.save()
        return JsonResponse({'message': post.likes})
    else:
        likefilter.delete()
        post.likes=post.likes-1
        post.save()
        return JsonResponse({'message': post.likes})

@login_required(login_url='signin')
def deletepost(request):
    
    if request.method=="POST":
        postid=request.POST['postid']
        post=Post.objects.get(id=postid)
        
        a=(post.user)
        b=(request.user)
        if str(a)==str(b):
            post.image.delete()
            post.delete()
        else:
            print('post cant be deleted')
        
        return redirect(f"/profile/{a}")
    return redirect('/')


    
@login_required(login_url='signin')
def tempp(request):
    
    # photos = Photo.objects.all()
    form = ImageForm(request.POST or None,request.FILES or None)
    user_profile=Profile.objects.get(user=request.user)
    if user_profile.mail_verification == False:
        return redirect('/mail_verification')
    # print(form)
    if form.is_valid():
        print('valid')
        photo=form.cleaned_data['file']
        user_profile.file.delete()
        user_profile.file=photo

        user_profile.save()
        # form.save()
        return redirect('/psettings')
    context = {'form': form}
    return render(request, 'crop.html', context)
   



def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password'] 
        
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            user_profile=Profile.objects.get(user=request.user)
            return redirect('/')
           
        else:
            messages.info(request,'Check username or Password')
            return redirect('signin')

    
    return render(request,'signin.html')  

@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')




@login_required(login_url='signin')
def upload(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('uphoto')
        
        caption=request.POST.get('caption')
        
        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return render(request,'upload.html')

@login_required(login_url='signin')
def psettings(request):
    user_profile=Profile.objects.get(user=request.user)
    
    if user_profile.mail_verification == False:
        return redirect('/mail_verification')
    
    
    

    if request.method=='POST':
        bio=request.POST['bio']
        fname=request.POST['fname']
        lname=request.POST['lname']
        location=request.POST['location']
        role=request.POST['role']
        status=request.POST['status']
        dob=request.POST['dob']
        # birthday=request.POST['birthday']
        
        user_profile.bio=bio
        # user_profile.birthday=birthday
        user_profile.lname=lname
        user_profile.fname=fname
        user_profile.role=role
        user_profile.dob=dob
        user_profile.status=status
        user_profile.location=location
        user_profile.save()
   
        return redirect('/psettings')


    return render(request,'psetting.html',{'user_profile':user_profile}) 


@login_required(login_url='signin') 
def profile(request,pk):

    userown=User.objects.get(username=request.user)
    user_own=Profile.objects.get(user=userown)
    if user_own.mail_verification == False:
        return redirect('//mail_verification')
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    posts=Post.objects.filter(user=pk)
    noofposts=len(posts)

    follower=request.user.username
    user=pk
    if followers.objects.filter(follower=follower,user=user).first():
        buttontxt='Unfollow'
    else:
        buttontxt='Follow'

    user_followers=len(followers.objects.filter(user=pk))
    user_following=len(followers.objects.filter(follower=pk))
    
    # userfoolowing profile
    userfollowinglist=[]
    userfpdata=[]
    userf=followers.objects.filter(follower=request.user.username)
    for u in userf:
        userfollowinglist.append(u.user)
    for k in userf:
        uuu=User.objects.get(username=k.user)
        ppp=Profile.objects.get(id_user=uuu.id)
        userfpdata.append(ppp)        

    likedposts=Likepost.objects.filter(username=request.user)
    likedpostsid=[]
    for i in likedposts:
        likedpostsid.append(i.postid)

    context={'user_object':user_object,
    'user_own':user_own,
    'user_profile':user_profile,
    'posts':posts,
    'noofposts':noofposts,
    'buttontxt':buttontxt,
    'user_followers':user_followers,
    'user_following':user_following,
    'userfollowing':userfpdata,
    'likedpostsid':likedpostsid
    }

    return render(request,'profile.html',context) 

@login_required(login_url='signin') 
def follow(request):
    userown=User.objects.get(username=request.user)
    user_own=Profile.objects.get(user=userown)
    if user_own.mail_verification == False:
        return redirect('/mail_verification')
    if request.method=='POST':
        follower=request.POST.get('follower')
        user=request.POST.get('user')

        if followers.objects.filter(follower=follower,user=user).first():
            unfollow=followers.objects.get(follower=follower,user=user)
            unfollow.delete()
            return redirect('/profile/'+user)
        else:
            newfollow=followers.objects.create(follower=follower,user=user)
            newfollow.save()
            return redirect('/profile/'+user)

              
    else:
        return redirect("/")

@login_required(login_url='signin')
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    # userown=User.objects.get(username=request.user)
    # user_own=Profile.objects.get(user=userown)
    if user_profile.mail_verification == False:
        return redirect('/mail_verification')
    
    if request.method=='POST':
        searchname=request.POST['searchu']
        username_object=User.objects.filter(username__icontains=searchname)

        username=[]
        username_profilelist=[]
        for users in username_object:
            username.append(users.id)

        for ids in username:
            pl=Profile.objects.filter(id_user=ids)
            username_profilelist.append(pl)

        usplist=list(chain(*username_profilelist))
        return render(request,'search.html',{'user_profile':user_profile,'usplist':usplist,'on':0})

    alll=User.objects.all()
    userf=followers.objects.filter(follower=request.user.username)
    user_following_all = []
    for user in userf:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    new_suggestions_list = [x for x in list(alll) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        # print(users.id)
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    lsugg = list(chain(*username_profile_list))


    return render(request,'search.html',{'user_profile':user_profile,'on':1,'lsugg':lsugg})


def crop(request):
    return render(request,'crop.html')






def cover(request):
    # photos = Photo.objects.all()
    form = ImageForm(request.POST or None,request.FILES or None)
    user_profile=Profile.objects.get(user=request.user)
    
    # print(form)
    if form.is_valid():
        print('valid')
        photo=form.cleaned_data['file']
        
        user_profile.cover.delete()
        user_profile.cover=photo
        user_profile.save()
        # form.save()
        return redirect('/psettings')
    context = {'form': form}
    return render(request, 'cover.html', context)

def youfollows(request):
    userown=User.objects.get(username=request.user)
    user_own=Profile.objects.get(user=userown)
    followsme=[]
    username_profilelist=[]
    check=followers.objects.all()
    # print(check)
    for i in check:
        if(i.follower==str(request.user)):
        #    print(i.follower,request.user)
           followsme.append(i.user)
    username=[]
    username_profilelist=[]
    for f in followsme:
        username_object=User.objects.get(username=f)
        username.append(username_object.id)
    for ids in username:
        pl=Profile.objects.filter(id_user=ids)
        username_profilelist.append(pl)
    usplist=list(chain(*username_profilelist))
    print(usplist)
    return render(request,'search.html',{'user_profile':user_own,'usplist':usplist})

def followsme(request):
    userown=User.objects.get(username=request.user)
    user_own=Profile.objects.get(user=userown)
    followsme=[]
    username_profilelist=[]
    check=followers.objects.all()
    # print(check)
    for i in check:
        if(i.user==str(request.user)):
        #    print(i.follower,request.user)
           followsme.append(i.follower)
    username=[]
    username_profilelist=[]
    for f in followsme:
        username_object=User.objects.get(username=f)
        username.append(username_object.id)
    for ids in username:
        pl=Profile.objects.filter(id_user=ids)
        username_profilelist.append(pl)
    usplist=list(chain(*username_profilelist))
    print(usplist)
    return render(request,'search.html',{'user_profile':user_own,'usplist':usplist})

@login_required(login_url='signin')
def chat(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    if user_profile.mail_verification == False:
        return redirect('/mail_verification')
    user=request.user
    total=messageroom.objects.filter(sender=user)
   
    
    userown=User.objects.get(username=request.user)
    user_own=Profile.objects.get(user=userown)
    user2=request.user
    total=messageroom.objects.filter(sender=user2)
    chatlist=[]
    for i in total:
        chatlist.append(i.reci)
    rtotal=messageroom.objects.filter(reci=user2)
    for i in rtotal:
        chatlist.append(i.sender)
    
    ports=messageroom.objects.all().order_by('lastmessage')
    
    portlist=[]
    for p in ports:
        
        if str(p.sender) == str(request.user):
            portlist.append(p.reci)
        elif str(p.reci) == str(request.user):
            portlist.append(p.sender)

    
        
    portlist.reverse()
    username=[]
    username_profilelist=[]
    for f in portlist:
        username_object=User.objects.get(username=f)
        username.append(username_object.id)
    for ids in username:
        pl=Profile.objects.filter(id_user=ids)
        username_profilelist.append(pl)

    alllist=[]
    apl=Profile.objects.all()
    alllist.append(apl)
    allprof=list(chain(*alllist))
    usplist=list(chain(*username_profilelist))

    
    return render(request,'chathere.html',{'userown':user_own,'usplist':usplist,'user_profile':user_profile,'allprof':allprof})
   

@login_required(login_url='signin')
def chatroom(request,pk):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    if user_profile.mail_verification == False:
        return redirect('/mail_verification')
    reci=pk
    pk2=User.objects.get(username=pk)
    pk_profile=Profile.objects.get(user=pk2)

    sender=User.objects.get(username=request.user)
    # print(reci,sender)

    r1=messageroom.objects.filter(reci=reci,sender=request.user.username).first()
    if r1 is None:
        r2=messageroom.objects.filter(sender=reci,reci=request.user.username).first()
        if r2 is None:
            new=messageroom.objects.create(reci=reci,sender=request.user.username)
            new.save()
            mrid=messageroom.objects.filter(reci=reci,sender=request.user.username).first()
            mid=mrid.messageroomid
        else:
            mid=r2.messageroomid
    else:
        mid=r1.messageroomid
    
    userown=User.objects.get(username=request.user)
    user_own=Profile.objects.get(user=userown)
    user2=request.user
    total=messageroom.objects.filter(sender=user2)
    chatlist=[]
    for i in total:
        chatlist.append(i.reci)
    rtotal=messageroom.objects.filter(reci=user2)
    for i in rtotal:
        chatlist.append(i.sender)
    
    ports=messageroom.objects.all().order_by('lastmessage')
    
    portlist=[]
    for p in ports:
        
        if str(p.sender) == str(request.user):
            portlist.append(p.reci)
        elif str(p.reci) == str(request.user):
            portlist.append(p.sender)

    
        
    portlist.reverse()
    username=[]
    username_profilelist=[]
    for f in portlist:
        username_object=User.objects.get(username=f)
        username.append(username_object.id)
    for ids in username:
        pl=Profile.objects.filter(id_user=ids)
        username_profilelist.append(pl)

    alllist=[]
    apl=Profile.objects.all()
    alllist.append(apl)
    allprof=list(chain(*alllist))
    usplist=list(chain(*username_profilelist))

    print('allp',allprof)
    return render(request,'messenger.html',{'mid':mid,'userown':user_own,'pk':pk_profile,'usplist':usplist,'user_profile':user_profile,'allprof':allprof})

def sendm(request):
    message=request.POST['message']
    username=request.POST['usernade']
    roomid=request.POST['roomid']

    newm=cmessage.objects.create(value=message,room=roomid,sender=username)
    newm.save()
    updatetam=messageroom.objects.get(messageroomid=roomid)
    updatetam.lastmessage=newm.samya
    updatetam.save()
    return HTTPResponse('good')

def getm(request,rr):
    # room=messageroom.objects.get(messageroomid=rr)
    allmessage=cmessage.objects.filter(room=rr)
    return JsonResponse({"messages":list(allmessage.values())})

@login_required(login_url='signin')
def searchchat(request):
    string=request.POST['string']
    
    username_object=User.objects.filter(username__icontains=string)

    usernamee=[]
    userl=[]
    username_profilelist=[]
    for users in username_object:
        usernamee.append(users.id)
        userl.append(users.username)
    for ids in usernamee:
        pl=Profile.objects.filter(id_user=ids)
        username_profilelist.append(pl)
    usplist=list(chain(*username_profilelist))
    if string=="":
        userl=[]

    return JsonResponse({"messages":list(userl)})

def maik(request):
     
    # az=[]
    # email="afsarbande002@gmail.com"
    # az.append(email)
    id=120
    # html_content=render_to_string("image.html",{'title':'testing','content':id})
    # textc=strip_tags(html_content)
    # emai=EmailMultiAlternatives('Order dertails',textc, settings.DEFAULT_FROM_EMAIL,az)
    # emai.attach_alternative(html_content,'text/html')
    # emai.send()
    return render(request,'image.html')

def forgotpass(request):

    emaill='nothing'
    otpsend=False
    if request.method=='POST':
        emaill=request.POST['emaill']
        user_obj=User.objects.filter(email=emaill)
        

        if len(user_obj)==0:
            print('usernone')
            otpsend=False
            respons='User not found'
            return JsonResponse({'otpsend': otpsend,'respons':respons})
        else:
            user_dd=User.objects.get(email=emaill)
            user_profile=Profile.objects.get(user=user_dd)
            fnameofuser=user_profile.fname
            otpsend=True
            print('something')
            respons='OTP send successfully'
            range_start = 10**(6-1)
            range_end = (10**6)-1
            ottp= randint(range_start, range_end)
            user_otp=saveotp.objects.filter(email=emaill)
            if len(user_otp)==0:
                new_user_otp=saveotp.objects.create(email=emaill,otp=ottp)
                new_user_otp.save()
            else:
                
                user_otp[0].otp=ottp
                user_otp[0].save()

            az=[]
            az.append(emaill)
            try:
                pass
                html_content=render_to_string("image.html",{'title':'OTP','content':ottp,'requs':fnameofuser})
                textc=strip_tags(html_content)
                emai=EmailMultiAlternatives('OTP',textc, settings.DEFAULT_FROM_EMAIL,az)
                emai.attach_alternative(html_content,'text/html')
                emai.send()
            except Exception as e:
                print(str(e))
                return JsonResponse({'otpsend': False,'respons':str(e)})
            
            return JsonResponse({'otpsend': otpsend,'respons':respons})
            
    return render(request,'confirm_email.html',{'otpsend':otpsend,'igot':emaill})

def verify_otp(request):
    if request.method=='POST':
        emaill=request.POST['emaill']
        otp_filled=request.POST['otp']
        user_otp=saveotp.objects.filter(email=emaill)
        if(user_otp[0].otp==otp_filled):
            print("Matched")
            return JsonResponse({'result':True,'message':'Verified'})
            # user_obj=User.objects.get(email=emaill)
            # user_profile=Profile.objects.get(user=user_obj)
            # user_obj.set_password("Param0")
            # user_obj.save()
        else:
            print("Not Matching")
            return JsonResponse({'result':False,'message':'OTP is not matching'})

    return redirect('/forgotpass')
     
def changepass(request):
    if request.method=='POST':
        emaill=request.POST['emaill']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        # user_obj=User.objects.filter(email=emaill)
        if pass1==pass2 and len(pass1)!=0:
            user_obj=User.objects.get(email=emaill)
            
            user_obj.set_password(pass1)
            user_obj.save()
            return JsonResponse({'passchange':True,'message':'Password changed!'})
        elif len(pass1)==0:
            return JsonResponse({'passchange':False,'message':'Password can`t be empty'})
        else:
            return JsonResponse({'passchange':False,'message':'Password are not matching'})

    return redirect('/forgotpass')
