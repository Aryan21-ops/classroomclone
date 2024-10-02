from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
# Create your views here.
from accounts import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUp(CreateView):
    model = User
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"
