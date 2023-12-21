from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # You may add more validation and error handling as needed

        # Create user
        try:
            user = User.objects.create_user(username=username, password=password)
        except:
            return render(request, 'account/register.html', {'error': 'Already exist'})
        login(request, user)
        return redirect('home')  # Redirect to the desired page after registration

    return render(request, 'account/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the desired page after login
        else:
            # Authentication failed, handle accordingly
            return render(request, 'account/login.html', {'error': 'Invalid credentials'})

    return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
