from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.views import generic
from . import models
from .forms import CommentForm
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


class PostList(generic.ListView):
    model = models.Post


class PostDetail(LoginRequiredMixin, generic.DetailView, FormMixin):
    model = models.Post
    template_name = 'post/post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post:post_single', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['commentform'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)

        comment.post = self.get_object()
        comment.user = self.request.user
        form.save()
        return super().form_valid(form)


class CreatePost(LoginRequiredMixin, generic.CreateView):

    fields = ('message', 'group')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = models.Post

    slug = ''

    def get_success_url(self):
        group_slug = self.slug
        return reverse_lazy("group:class_single", kwargs={'slug': group_slug})

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):

        group = self.get_object().group
        self.slug = group.slug
        return super().delete(*args, **kwargs)


def deletecomment(request, comment_id):
    if request.mehtod == 'POST':
        comment = models.Comment.objects.get(id=comment_id)
        post = comment.post
        comment.delete()
        return reverse('post:post_single', kwargs={'pk': post.pk})
