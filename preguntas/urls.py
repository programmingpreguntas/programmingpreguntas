from django.conf.urls import url

from . import views

app_name = 'preguntas'

urlpatterns = [
    url(r'^profile/(?P<usuario_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^questions/?P<question_id>[0-9]+)/$', views.question, name='question'),
]
