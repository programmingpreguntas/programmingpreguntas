from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Question, Answer, Usuario
from .serializers import QuestionSerializer, AnswerSerializer, UsuarioSerializer


def profile(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    question_set = Question.objects.filter(owner_id=usuario_id)
    questions_answered_set = Answer.objects.filter(owner_id=usuario_id)
    context = {'usuario': usuario, 'question_set': question_set,
               'questions_answered_set': questions_answered_set}
    return render(request, 'preguntas/profile.html', context)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    queryset = Question.objects.all().order_by('created')
    serializer_class = QuestionSerializer
    print("HELLO THIS IS ALEX")


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
