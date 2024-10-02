from django import forms
from .models import Assignment, ResponseFiles, AssignmentFiles


class AssignmentForm(forms.ModelForm):
    deadline = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False,
                                   widget=forms.DateTimeInput(attrs={
                                       'class': 'form-control datetimepicker-input',
                                       'data-target': '#datetimepicker1'
                                   }))
    task = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '3',
    }))

    class Meta:
        model = Assignment
        fields = ('title', 'task', 'deadline')


class AssignmentFilesForm(forms.ModelForm):
    attachments = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control ',
    }))

    class Meta:
        model = AssignmentFiles
        fields = ('attachments',)


class ResponseForm(forms.ModelForm):
    rfiles = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = ResponseFiles
        fields = ('rfiles',)
