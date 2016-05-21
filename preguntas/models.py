from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Usuario(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.name


class Comment(models.Model):
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='comment_voted_up')
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


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='question_voted_up')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title


class Answer(models.Model):
    body = models.TextField()
    upvotes = models.ManyToManyField(Usuario, related_name='answer_voted_up')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Usuario)
    question = models.ForeignKey(Question)
    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ('owner', 'question')

    def __str__(self):
        return self.body[:50]
