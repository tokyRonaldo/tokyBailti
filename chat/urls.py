from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.conversation_list, name="conversation_list"),
    path("<int:pk>/", views.conversation_room, name="conversation_room"),
]
