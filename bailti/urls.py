
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('dashboard', views.dashboard,name="dashboard"),
    path('property', views.property,name="property"),
    path('property/create', views.property_create,name="property_create"),
    path('locataire', views.locataire,name="locataire"),
    path('locataire/create', views.locataire_create,name="locataire_create"),
    path('locataire/store', views.locataire_store,name="locataire_store"),
    path('locations', views.locations,name="locations"),
    path('locations/create', views.location_create,name="location_create"),
    path('favorie', views.favorie,name="favorie"),
]
