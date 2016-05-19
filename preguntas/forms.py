from django import forms
from .models import Question, Answer


class QuestionForm(forms.Modelform):
    title = forms.CharField(max_length=255,
                            help_text="Please enter question title.")
    body = forms.TextField(help_text='Please write your question.')

    class Meta:
        model = Question
        fields = ('title', 'body')


class AnswerForm(forms.Modelform):
    body = forms.TextField(help_text="Please write your answer.")

    class Meta:
        model = Answer
        fields = ('body')
