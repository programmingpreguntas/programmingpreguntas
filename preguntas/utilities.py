import random
import string
from .models import Question, Answer, Usuario
from django.contrib.auth.models import User
from psycopg2 import IntegrityError as psyIntegrityError
from django.db.utils import IntegrityError as djaIntegrityError
import re
from django.db.models import Q


RANDOM_TEXT = open("preguntas/lorem.txt", "r").read()


def make_text(characters):
    start = random.randint(0, len(RANDOM_TEXT) - characters - 1)
    return(RANDOM_TEXT[start:start + characters])


def make_name():
    raw = make_text(random.randint(10, 25)).lower()
    include = (string.ascii_lowercase)
    stripped = ''.join(ch for ch in raw if ch in include)
    break_char = random.randint(3, len(stripped)-3)
    first_name = stripped[0:break_char]
    last_name = stripped[break_char:]
    return first_name + " " + last_name


def make_username():
    raw = make_text(random.randint(5, 10)).lower()
    include = (string.ascii_lowercase)
    stripped = ''.join(ch for ch in raw if ch in include)
    return stripped


def make_random_user():
    try:
        User.objects.create_user(username=make_username(),
                                 password="password123")
    except psyIntegrityError:
        make_random_user()
    except djaIntegrityError:
        make_random_user()


def make_random_users(num):
    for _ in range(num):
        make_random_user()


def make_random_usuarios():
    for each_User in User.objects.all():
        Usuario(user=each_User, name=make_name()).save()


def make_random_questions():
    for each_usuario in Usuario.objects.all():
        for _ in range(random.randint(0, 10)):
            Question(title=make_text(random.randint(25, 255)),
                     body=make_text(random.randint(50, 5000)),
                     owner=each_usuario
                     ).save()


def make_random_answers():
    number_of_usuarios = Usuario.objects.count()
    for each_question in Question.objects.all():
        for _ in range(random.randint(0, 25)):
            try:
                Answer(body=make_text(random.randint(25, 7500)),
                       question=each_question,
                       owner=Usuario.objects.all()[random.randint(0, number_of_usuarios-1)]
                       ).save()
            except psyIntegrityError, djaIntegrityError:
                continue



def make_random_votes():
    number_of_questions = Question.objects.count()
    number_of_answers = Answer.objects.count()
    for each_usuario in Usuario.objects.all():
        for _ in range(random.randint(0, 50)):
            this_question_index = random.randint(0, number_of_questions-1)
            this_question = Question.objects.all()[this_question_index]
            this_question.upvotes.add(each_usuario)
        for _ in range(random.randint(0, 200)):
            this_answer_index = random.randint(0, number_of_answers-1)
            this_answer = Answer.objects.all()[this_answer_index]
            this_answer.upvotes.add(each_usuario)


def make_random_data():
    print("Making Users")
    make_random_users(100)
    print("Making Usuarios")
    make_random_usuarios()
    print("Asking Questions")
    make_random_questions()
    print("Getting Answers")
    make_random_answers()
    print("Voting")
    make_random_votes()


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
