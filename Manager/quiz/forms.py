from django import forms
from .models import QuizTest, Question


class QuizForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3
    }))
    quizname = forms.CharField(label='Test Name', required=True)

    class Meta:
        model = QuizTest
        fields = ('quizname', 'description', 'test_interval', 'test_starttime')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('quiz', 'qimage',)
