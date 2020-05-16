from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        #user wants to sign up now
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':'Username already exists.'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'Passwords must match'})

    else:
        #user wants to fill data
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'] ,password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Invalid Credentials'})
    else:
        return render(request, 'accounts/login.html')

def signout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
