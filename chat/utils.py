# utils dans chat/utils.py
from bailti.models import Conversation

def get_or_create_conversation(user1, user2, title=None):
    # chercher une conversation avec exactement ces 2 participants
    qs = Conversation.objects.filter(participants=user1).filter(participants=user2)
    for conv in qs:
        if conv.participants.count() == 2:
            return conv
    conv = Conversation.objects.create(title=title)
    conv.participants.add(user1, user2)
    return conv