from django.conf.urls import url

from . import views

app_name = 'preguntas'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<usuario_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^questions/$', views.QuestionList.as_view(), name='questions'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^search_questions/', views.search, name='search'),
    url(r'^login/auth_view/$', views.auth_view, name='auth'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question_detail,
        name='question'),
    url(r'new_question/$', views.new_question, name='new_question')
]
