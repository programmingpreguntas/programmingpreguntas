from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=255,
                            help_text="Please enter question title: ")
    body = forms.CharField(help_text='Please write your question: ',
                           widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ('title', 'body')


class AnswerForm(forms.ModelForm):
    body = forms.CharField(help_text="Please write your answer: ",
                           widget=forms.Textarea)

    class Meta:
        model = Answer
        fields = ('body',)
