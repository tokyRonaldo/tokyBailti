
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.listUsers,name="list_users"),
]
