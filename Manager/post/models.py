from django.conf import settings
from django.urls import reverse
from django.db import models


from group.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User, related_name="users_posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    group = models.ForeignKey(
        Group, related_name="group_posts", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message} of {self.group.name}'

    def get_absolute_url(self):
        return reverse(
            "post:post_single",
            kwargs={
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]


class Comment(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message} by {self.user.username}'

    class Meta:
        ordering = ["-created_at"]
