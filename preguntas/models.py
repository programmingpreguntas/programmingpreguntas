from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Usuario(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.name

    def _get_votable_points(self, VotableType):
        my_votables = VotableType.objects.filter(owner=self)
        votable_up_points = my_votables.annotate(points=Count('upvotes')).aggregate(sum=Sum('points'))['sum']
        votable_down_points = my_votables.annotate(points=Count('downvotes')).aggregate(sum=Sum('points'))['sum']
        if votable_up_points is None:
            votable_up_points = 0
        if votable_down_points is None:
            votable_down_points = 0
        return votable_up_points - votable_down_points

    def get_points(self):
        question_points = self._get_votable_points(Question)
        answer_points = self._get_votable_points(Answer)
        comment_point = self._get_votable_points(Comment)
        return question_points + answer_points + comment_point


class Comment(models.Model):
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='comment_voted_up')
    downvotes = models.ManyToManyField(Usuario, related_name='comment_voted_down')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.body[:50]

    def get_question_id(self):
        if self.content_object.__class__.__name__ == 'Question':
            return self.content_object.id
        elif self.content_object.__class__.__name__ == 'Answer':
            return self.content_object.question.id
        else:
            return None

    def get_score(self):
        return self.upvotes.count() - self.downvotes.count()

    def voted_down_by(self, usuario):
        return self.downvotes.filter(id=usuario.id).exists()

    def voted_up_by(self, usuario):
        return self.upvotes.filter(id=usuario.id).exists()


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='question_voted_up')
    downvotes = models.ManyToManyField(Usuario, related_name='question_voted_down')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comments.all()

    def get_score(self):
        return self.upvotes.count() - self.downvotes.count()

    def voted_down_by(self, usuario):
        return self.downvotes.filter(id=usuario.id).exists()

    def voted_up_by(self, usuario):
        return self.upvotes.filter(id=usuario.id).exists()


class Answer(models.Model):
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='answer_voted_up')
    downvotes = models.ManyToManyField(Usuario, related_name='answer_voted_down')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario)
    question = models.ForeignKey(Question)
    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ('owner', 'question')

    def __str__(self):
        return self.body[:50]

    def get_comments(self):
        return self.comments.all()

    def get_score(self):
        return self.upvotes.count() - self.downvotes.count()

    def voted_down_by(self, usuario):
        return self.downvotes.filter(id=usuario.id).exists()

    def voted_up_by(self, usuario):
        return self.upvotes.filter(id=usuario.id).exists()
