from django.conf.urls import url

from . import views

app_name = 'preguntas'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<usuario_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question_detail,
        name='question'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'new_question/$', views.new_question, name='new_question')
]
