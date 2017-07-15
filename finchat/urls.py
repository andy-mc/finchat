"""finchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

from chat.views import SignUpView, UserDetail, HomeView, chat_room


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(HomeView.as_view()), name='home'),
    url(r'^(?P<label>[\w-]{,50})/$', chat_room, name='chat_room'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/signup/$', SignUpView.as_view(), name="signup"),
    url(r'^users/(?P<pk>[-\w]+)/$',
        login_required(UserDetail.as_view()), name='user-detail'),
]
