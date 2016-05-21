from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User


class Usuario(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.name

    def _get_votable_points(self, Votable):
        my_votables = Votable.objects.filter(owner=self)
        votable_points = my_votables.annotate(points=Count('upvotes')).aggregate(sum=Sum('points'))['sum']
        return votable_points

    def get_points(self):
        question_points = self._get_votable_points(Question)
        answer_points = self._get_votable_points(Answer)
        return question_points + answer_points



class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='question_voted_up')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario)

    def __str__(self):
        return self.title

    def get_score(self):
        return self.upvotes.count()

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

    def get_score(self):
        return self.upvotes.count()
