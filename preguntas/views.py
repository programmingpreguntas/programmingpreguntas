import uuid
from django.shortcuts import render, get_object_or_404, render_to_response
from rest_framework import viewsets
from .models import Question, Answer, Usuario
from .serializers import QuestionSerializer, AnswerSerializer, UsuarioSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from .utilities import get_query
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from .forms import AnswerForm, QuestionForm



def profile(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    question_set = Question.objects.filter(owner_id=usuario_id)
    questions_answered_set = Answer.objects.filter(owner_id=usuario_id)
    try:
        date = request.GET['date']
        if date:
            questions_answered_set = questions_answered_set.order_by('-created')
    except KeyError:
        pass
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
    context = {}
    top_list = Question.objects.all().order_by('-created')[:20]
    try:
        terms = request.GET['search']
        context['terms'] = terms
        found_questions = Question.objects.filter(body__icontains=terms)
        context['found_questions'] = found_questions
    except KeyError:
        pass
    context['top_list'] = top_list
    return render(request, 'preguntas/question_list.html', context)



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


def question_redirect(request, question_id):
    url = '/preguntas/question/{}/'.format(question_id)
    return HttpResponseRedirect(url)

def question_detail(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = Question.objects.get(id=question_id)
            try:
                answer.owner = Usuario.objects.get(id=request.user.usuario.id)
            except AttributeError:
                answer.owner = Usuario.objects.get(id=163) # if anon user, make it user 163 for now.
            answer.save()
            return question_redirect(request, question_id)
        else:
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = AnswerForm()
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question_id=question.id)
    context = {'form': form,
               'question': question,
               'answers': answers}
    return render(request, 'preguntas/question.html', context)

def new_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            try:
                question.owner = Usuario.objects.get(id=request.user.usuario.id)
            except AttributeError:
                question.owner = Usuario.objects.get(id=163) # if anon user, make it user 163 for now.
            question.save()
            return question_redirect(request, question.id)
        else:
            print(form.errors)
    else:
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'preguntas/new_question.html', context)
