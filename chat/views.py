from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.db.models import Q
from django.conf import settings
from bailti.models import Conversation, Message ,Locataire
from django.template.loader import render_to_string
from .utils import get_or_create_conversation



User = get_user_model()

@login_required
def conversation_list(request):
    locataires = Locataire.objects.filter(proprietaire_user_id = request.user.id)
    convs = request.user.conversations.all().order_by("-created_at")
    for c in convs:
        c.other_user = c.participants.exclude(id=request.user.id).first()
    return render(request, "chat/conversation_list.html", {"conversations": convs,"locataires" : locataires})

@login_required
def conversation_room(request, pk):
    conv = get_object_or_404(Conversation, pk=pk)
    if request.user not in conv.participants.all():
        return redirect("chat:conversation_list")
    destinateur = conv.participants.exclude(id=request.user.id).first()
    messages = conv.messages.select_related("sender").all()
    return render(request, "chat/room.html", {
        "conversation": conv,
        "messages": messages,
        "destinateur": destinateur,
        "WS_PORT": settings.WEBSOCKET_PORT,
        "WS_HOST": settings.WEBSOCKET_HOST,
        "WS_SCHEME": settings.WEBSOCKET_SCHEME,
        })

@login_required
def new_conversation(request):
    if request.method == "POST":
        locataire_id = request.POST.get("locataire")

        # Vérifier si un locataire a été sélectionné
        if not locataire_id:
            messages.error(request, "Veuillez sélectionner un locataire.")
            return redirect("chat:conversation_list")  # la page où le modal était

        # Récupérer le locataire
        locataire = Locataire.objects.filter(id=locataire_id).first()

        if not locataire:
            messages.error(request, "Locataire introuvable.")
            return redirect("chat:conversation_list")

        # Créer ou récupérer la conversation
        conv = get_or_create_conversation(request.user, locataire.user_locataire)

        return redirect("chat:conversation_room", pk=conv.id)

    return redirect("chat:conversation_list")