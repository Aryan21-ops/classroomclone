from django import forms


class JoinForm(forms.Form):
    code = forms.CharField(max_length=8, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Enter Code', 'class': 'mt-3'}))
