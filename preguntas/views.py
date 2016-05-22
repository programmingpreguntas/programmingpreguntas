import uuid
from django.shortcuts import render, get_object_or_404, render_to_response
from rest_framework import viewsets
from .models import Question, Answer, Usuario, Comment
from .serializers import QuestionSerializer, AnswerSerializer, UsuarioSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from .utilities import get_query, get_parent_obj
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from .forms import AnswerForm, QuestionForm, CommentForm
from django.apps import apps
from django.core.urlresolvers import reverse
from django.db.models import Count


def profile(request, usuario_id=None):
    if usuario_id is None:
        try:
            usuario_id = request.user.usuario.id
        except AttributeError:
            return render(request, 'preguntas/please_login.html')
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
            return super(ListView, self).get_queryset().order_by('-created')


# Search copied from http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
def search(request):
    query_string = ''
    found_questions = []
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        question_query = get_query(query_string, ['title', 'body', ])
        found_questions = Question.objects.filter(question_query)
    return QuestionList.as_view()(request, queryset=found_questions)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    queryset = Question.objects.all().annotate(score=Count("upvotes")).order_by('-score', '-created')
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    queryset = Answer.objects.all().annotate(score=Count("upvotes")).order_by('-score','-created')
    serializer_class = AnswerSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows abilities to be viewed or edited.
    """
    queryset = Usuario.objects.all().order_by('name')
    serializer_class = UsuarioSerializer


def index(request):
    context = {}
    question_list = Question.objects.all().order_by('-created')[:20]
    try:
        terms = request.GET['search']
        context['terms'] = terms
        found_questions = Question.objects.filter(body__icontains=terms)
        context['found_questions'] = found_questions
    except KeyError:
        pass
    context['question_list'] = question_list
    return render(request, 'preguntas/question_list.html', context)


def login_user(request):
    c = {}
    c.update(csrf(request))
    request.session['fav_color'] = 'blue'

    print(request.session)
    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            state = "You're successfully logged in"
            #return HttpResponse(state)
            #print(auth.user_logged_in)
            return HttpResponseRedirect('/profile/%s' % user.id)

        else:
            state = "Your account is not active, please contact the site admin."
            # context = {'errors': [state]}

            return HttpResponse(state)
            # return redirect()
    else:
        state = "Your username and/or password were incorrect."
        # context = {'errors': [state]}
        # return render(request, 'login.html', context)
        return HttpResponse(state)
        # return redirect()

def logout_user(request):
        auth.logout(request)
        return redirect(reverse('preguntas:questions'))
        #return HttpResponseRedirect('question')
        #return render_to_response('question')




def question_detail(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = Question.objects.get(id=question_id)
            answer.owner = Usuario.objects.get(id=request.user.usuario.id)
            answer.save()
            return HttpResponseRedirect(reverse('preguntas:question', args=(question_id,)))
        else:
            return HttpResponse("{}\n<a href='{}'>Back to Question".format(
                form.errors, reverse('preguntas:question', args=(
                    question_id,))))
    else:
        # If the request was not a POST, display the form to enter details.
        form = AnswerForm()
    question = Question.objects.get(id=question_id)
    question_comments = question.get_comments()
    answers = Answer.objects.filter(question_id=question.id).annotate(score=Count("upvotes")).order_by('-score','-created')
    i_have_answered = answers.filter(owner_id=request.user.usuario.id).exists()
    context = {'form': form,
               'question': question,
               'question_comments': question_comments,
               'answers': answers,
               'i_have_answered': i_have_answered}
    return render(request, 'preguntas/question.html', context)


def new_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            try:
                question.owner = Usuario.objects.get(id=request.user.usuario.id)
            except AttributeError:
                # if anon user, make it user 163 for now.
                question.owner = Usuario.objects.get(id=1)

            question.save()
            return HttpResponseRedirect(reverse('preguntas:question', args=(question.id,)))
        else:
            return HttpResponse("{}\n<a href='{}'>Back to New Question".format(
                form.errors, reverse('preguntas:new_question')))
    else:
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'preguntas/new_question.html', context)


def new_comment(request, parent_type, parent_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            try:
                comment.owner = Usuario.objects.get(id=request.user.usuario.id)
            except AttributeError:
                # if anon user, make it user 163 for now.
                comment.owner = Usuario.objects.get(id=100)
            comment.content_object = get_parent_obj(parent_type, parent_id)
            comment.save()
            question_id = comment.get_question_id()
            return HttpResponseRedirect(reverse('preguntas:question',
                                                args=(question_id,)))
        else:
            return HttpResponse("{}\n<a href='{}'>Back to New Comment".format(
                form.errors, reverse('preguntas:new_comment', args=(
                    parent_type, parent_id))))
    else:
        parent_obj = get_parent_obj(parent_type, parent_id)
        form = CommentForm()
        context = {'form': form,
                   'parent_obj': parent_obj,
                   'parent_name': parent_obj.__class__.__name__}
        return render(request, 'preguntas/new_comment.html', context)


def vote(request):
    if request.method == "POST":
        model_name = request.POST['votable_type']
        vote_id = request.POST['votable_id']
        preguntas_config = apps.get_app_config("preguntas")
        votable = preguntas_config.get_model(model_name).objects.get(id=vote_id)
        try:
            votable.upvotes.add(Usuario.objects.get(id=request.user.usuario.id))
        except AttributeError:
            votable.upvotes.add(Usuario.objects.get(id=1))

    return HttpResponseRedirect(request.POST['this_url'])
