from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from preguntas import views

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'usuarios', views.UsuarioViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'programmingpreguntas.views.home', name='home'),
    #url(r'^$', include('preguntas.urls')),
    url(r'^', include('preguntas.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
