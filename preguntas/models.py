from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User


class Usuario(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.name

    def get_question_points(self):
        my_questions = Question.objects.filter(owner=self)
        return my_questions.annotate(points=Count('upvotes')).aggregate(Sum('points'))

class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='question_voted_up')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario)

    def __str__(self):
        return self.title


class Answer(models.Model):
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='answer_voted_up')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario)
    question = models.ForeignKey(Question)

    class Meta:
        unique_together = ('owner', 'question')

    def __str__(self):
        return self.body[:50]
