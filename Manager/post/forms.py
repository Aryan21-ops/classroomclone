from django import forms

from post import models


class PostForm(forms.ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '2',
        'placeholder': 'Share with your class',

    }))

    class Meta:
        fields = ['message']
        model = models.Post


class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '2'
    }))

    class Meta:
        fields = ['message']
        model = models.Comment
