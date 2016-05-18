from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
]
