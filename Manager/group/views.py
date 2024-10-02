from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
# Create your views here.
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views import generic, View
from group.models import Group, GroupMember
from . import models
from django.views.generic.edit import FormMixin
from post.forms import PostForm
from .forms import JoinForm
from post.models import Post
from django.db.models import Q
from quiz.forms import QuizForm


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group

    def form_valid(self, form):
        form.instance.creator = self.request.user


class ListGroup(LoginRequiredMixin, generic.ListView):
    model = Group

    def get(self, *args, **kwargs):
        form = JoinForm()
        object_list = Group.objects.filter(
            Q(creator=self.request.user) | Q(members=self.request.user)).distinct()
        context = {'object_list': object_list,
                   'allow_empty': True, 'form': form}
        return render(self.request, 'group/group_list.html', context)


class SingleClass(LoginRequiredMixin, generic.DetailView, FormMixin):
    model = Group
    form_class = PostForm

    def get_success_url(self):
        return reverse('group:class_single', kwargs={'slug': self.kwargs.get('slug')})

    def get_context_data(self, **kwargs):
        context = super(SingleClass, self).get_context_data(**kwargs)
        context['postform'] = PostForm()
        context['quizform'] = QuizForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.group = self.get_object()
        self.object.user = self.request.user
        form.save()
        return super().form_valid(form)


def Join(request):
    if request.method == 'GET':
        form = JoinForm()
        context = {'form': form, }
        return render(request, 'group/join.html', context)

    if request.method == 'POST':
        code = request.POST.get("code")
        print(code)
        group = get_object_or_404(Group, code=code)
        slug = group.slug
        try:
            GroupMember.objects.create(user=request.user, group=group)
        except IntegrityError:
            print(IntegrityError)
            messages.warning(
                request, ("Warning, already a member of {}".format(group.name)))
            return redirect("group:class_single", slug=slug)

        else:
            print('success')
            messages.success(
                request, "You are now a member of the {} group.".format(group.name))
        return redirect("group:class_single", slug=slug)


class JoinClass(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("group:class_single", kwargs={"slug": self.kwargs.get("slug")})

    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        group = get_object_or_404(Group, code=code)
        slug = group.slug

        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            print(IntegrityError)
            messages.warning(
                self.request, ("Warning, already a member of {}".format(group.name)))

        else:
            print('success')
            messages.success(
                self.request, "You are now a member of the {} group.".format(group.name))

        return super(JoinClass, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            print(IntegrityError)
            messages.warning(
                self.request, ("Warning, already a member of {}".format(group.name)))

        else:
            print('success')
            messages.success(
                self.request, "You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveClass(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("group:class_single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
