from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import CreateView, DetailView

from . import forms
from .models import Message


@login_required
def home(request):
    messages = Message.objects.order_by('timestamp')[:50]

    context = {
        'username': request.user.username,
        'messages': messages,
    }

    return render(request, "index.html", context)


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
    form_class = forms.UserCreationForm
    success_url = settings.LOGIN_URL
    template_name = "chat/signup.html"
