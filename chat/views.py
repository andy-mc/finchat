from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, View

from .forms import RoomForm, UserCreationForm
from .models import Message, Room
from .models import Message, Room


class HomeView(View):
    """
    A welcome page where the user can select a chat room
    """

    def get(self, request):
        rooms = Room.objects.order_by('label')

        context = {
            'username': request.user.username,
            'rooms': rooms,
            'form': RoomForm,
        }

        return render(request, "home.html", context)

    def post(self, request):
        form = RoomForm(request.POST)
        rooms = Room.objects.order_by('label')

        if form.is_valid():
            form.save()
            return redirect('chat_room', label=form.cleaned_data['label'])

        context = {
            'username': request.user.username,
            'rooms': rooms,
            'form': form,
        }

        return render(request, "home.html", context)


@login_required
def chat_room(request, label):
    # If the room with the given label doesn't exist,
    # automatically create a room.
    room, created = Room.objects.get_or_create(label=label)

    messages = room.messages.order_by('timestamp')[:50]

    context = {
        'username': request.user.username,
        'room': room,
        'messages': messages,
    }

    return render(request, "chat/room.html", context)


class UserDetail(DetailView):
    model = User
    template_name = "chat/user-detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['messages'] = Message.objects.filter(
            user=self.request.user
        ).order_by(
            '-timestamp'
        )
        return context_data


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = settings.LOGIN_URL
    template_name = "chat/signup.html"
