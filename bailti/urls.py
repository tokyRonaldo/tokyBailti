
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.dashboard,name="dashboard"),
    path('property', views.property,name="property"),
    path('property/create', views.property_create,name="property_create"),
    path('property/create/<int:id>/', views.property_create,name="property_edit"),
    path('property/store', views.property_store,name="property_store"),
    path('property/delete/<int:id>/', views.property_delete,name="property_delete"),
    path('property/update/<int:id>/', views.property_update,name="property_update"),
    path('locataire', views.locataire,name="locataire"),
    path('locataire/create/', views.locataire_create, name='locataire_create'),
    path('locataire/create/<int:id>/', views.locataire_create, name='locataire_edit'),
    path('locataire/store', views.locataire_store,name="locataire_store"),
    path('locataire/delete/<int:id>/', views.locataire_delete,name="locataire_delete"),
    path('locataire/update/<int:id>/', views.locataire_update,name="locataire_update"),
    path('proprietaire', views.proprietaire,name="proprietaire"),
    path('locations', views.locations,name="locations"),
    path('locations/create', views.location_create,name="location_create"),
    path('locations/create/<int:id>/', views.location_create,name="location_edit"),
    path('locations/store', views.location_store,name="location_store"),
    path('locations/delete/<int:id>/', views.location_delete,name="location_delete"),
    path('locations/update/<int:id>/', views.location_update,name="location_update"),
    path('favorie', views.favorie,name="favorie"),
    path('quittance', views.quittance,name="quittance"),
]
