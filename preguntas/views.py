from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Question, Answer, Usuario
from .serializers import QuestionSerializer, AnswerSerializer, UsuarioSerializer
from django.contrib.auth import authenticate, login
from django.template import loader
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.models import User


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


def index(request):
    top_list = Question.objects.all()[:20]
    return render(request, 'preguntas/question_page.html', {'top_list': top_list})


def login_user(request):
    state = "Please log in below..."
    username = password = ''

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(request.POST)

        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                # return redirect()

            else:
                state = "Your account is not active, please contact the site admin."
                # return redirect()
        else:
            state = "Your username and/or password were incorrect."
            # return redirect()

    context = {'state':state, 'username': username}
    return render(request, 'preguntas_box/login.html', {'state':state, 'username': username})
