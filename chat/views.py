from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from bailti.models import Conversation, Message ,Locataire
from django.template.loader import render_to_string
from .utils import get_or_create_conversation



User = get_user_model()

@login_required
def conversation_list(request):
    convs = request.user.conversations.all().order_by("-created_at")
    #locataire= Locataire.objects.filter(proprietaire_user_id = request.user.id).first()
    #get_or_create_conversation(request.user,locataire.user_locataire)
    return render(request, "chat/conversation_list.html", {"conversations": convs})

@login_required
def conversation_room(request, pk):
    conv = get_object_or_404(Conversation, pk=pk)
    if request.user not in conv.participants.all():
        return redirect("chat:conversation_list")
    messages = conv.messages.select_related("sender").all()
    return render(request, "chat/room.html", {"conversation": conv, "messages": messages})
