from django.shortcuts import render
from .models import User

# Create your views here.
def listUsers(request):
    users=User.objects.all()
    return render(request , 'bailti/home.html',{'users' : users})
