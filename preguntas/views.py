from django.shortcuts import render
from rest_framework import viewsets
from .models import Question, Answer, Usuario
from .serializers import QuestionSerializer, AnswerSerializer, UsuarioSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    queryset = Question.objects.all().order_by('created')
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    queryset = Answer.objects.all().order_by('created')
    serializer_class = AnswerSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    queryset = Usuario.objects.all().order_by('name')
    serializer_class = UsuarioSerializer

class BreakViewSet(viewsets.ModelViewSet):
    breaktribute = 'break'

    def breaky_break(self):
        print('Break')
