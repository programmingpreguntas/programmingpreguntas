from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Question, Answer, Usuario
from .serializers import QuestionSerializer, AnswerSerializer, UsuarioSerializer
from django.contrib.auth import authenticate, login
from django.template import loader
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from .utilities import get_query
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf



def profile(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    question_set = Question.objects.filter(owner_id=usuario_id)
    questions_answered_set = Answer.objects.filter(owner_id=usuario_id)
    context = {'usuario': usuario, 'question_set': question_set,
               'questions_answered_set': questions_answered_set}
    return render(request, 'preguntas/profile.html', context)


class QuestionList(ListView):
    model = Question
    paginate_by = 25

    def get_queryset(self):
        if 'queryset' in self.kwargs:
            return self.kwargs['queryset']
        else:
            return super(ListView, self).get_queryset()


# Search copied from http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
def search(request):
    query_string = ''
    found_questions = []
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        question_query = get_query(query_string, ['title', 'body', ])
        found_questions = Question.objects.filter(question_query)
        # context = {
        #            'query_string': query_string,
        #            'found_questions': found_questions
        #            }
    # return HttpResponse("Searched for " + query_string +
    #                     " found " + str(len(found_questions)) + " questions.")
    return QuestionList.as_view()(request, queryset=found_questions)
    # return render(request, 'search/search_results.html',
    #               context=context)


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
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            state = "You're successfully logged in!"
            return HttpResponse(state)
            # return redirect()

        else:
            state = "Your account is not active, please contact the site admin."
            # context = {'errors': [state]}

            return HttpResponse(state)
            # return redirect()
    else:
        state = "Your username and/or password were incorrect."
        context = {'errors': [state]}
        return render(request, 'login.html', context)
        #return HttpResponse(state)
        # return redirect()
