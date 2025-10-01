from django.shortcuts import render, redirect
from . import views
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages #Allows us to send messages to the frontend

# Create your views here.

def index(request):
    return render(request, 'index.html')

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
        else:
            messages.info(request, 'Password do not match')
            return redirect('signup') #Redirects the user to the signup
            
        
    else:
        return render(request, 'signup.html')