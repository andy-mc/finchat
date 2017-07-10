from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Message


@login_required
def home(request):
    messages = Message.objects.all()[:50]

    context = {
        'username': request.user.username,
        'messages': messages,
    }

    return render(request, "index.html", context)
