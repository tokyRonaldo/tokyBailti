from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm
import sys

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            messages.success(request, "Inscription réussie ✅")
            return redirect('dashboard')
    else:
        print('testtttttttttttttttt2')
        form = RegisterForm()
    return render(request, 'app_user/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print('herrrr')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            print('atoooo')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Nom d’utilisateur ou mot de passe incorrect ❌")
    return render(request, 'app_user/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
