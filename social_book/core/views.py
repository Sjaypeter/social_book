from .models import Post, Profile
from django.shortcuts import render, redirect
from . import views
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages #Allows us to send messages to the frontend
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='signin') #Redirects the user to the sign in url
def index(request):
    user_object = User.objects.get(username = request.user.username) #Object of cureently logged in user
    user_profile = Profile.objects.get(user=user_object)
    
    posts=Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts':posts})

def signup(request):
    
    if request.method == 'POST':  #POST is for confidential info rather than GET
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                #Creates a profile for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
            
            
        else:
            messages.info(request, 'Password do not match')
            return redirect('signup') #Redirects the user to the signup
            
        
    else:
        return render(request, 'signup.html')
    
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
        
    return render(request, 'sign.html')


@login_required(login_url='signin') #Redirects the user to the sign in url
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None: #If no image is being sent it gets the urrent image the user has and submits
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('settings')
        
    return render(request, 'settings.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user= user, image=image, caption=caption)
        new_post.save()
        
    else:
        return redirect('/')
    return HttpResponse('<h1> Upload View</h1>')