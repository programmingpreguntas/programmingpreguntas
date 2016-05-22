from django.conf.urls import url

from . import views

app_name = 'preguntas'

urlpatterns = [
    url(r'^profile/$', views.profile, name='my_profile'),
    url(r'^profile/(?P<usuario_id>[0-9]*)/$', views.profile, name='profile'),
    url(r'^$', views.QuestionList.as_view(), name='questions'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^search/', views.search, name='search'),
    url(r'^login/auth_view/$', views.auth_view, name='auth_view'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question_detail,
        name='question'),
    url(r'^question/new$', views.new_question, name='new_question'),
    url(r'^comment/new/(?P<parent_type>[a-zA-Z]+)/(?P<parent_id>[0-9]+)/$',
        views.new_comment, name='new_comment'),
    url(r'^vote/$', views.vote, name="vote"),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    #url(r'^logout/question_list$', views.QuestionList.as_view(), name='questions'),
]
