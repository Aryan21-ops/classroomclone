from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class TodoTasks(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField(blank=True, null=True)
    task_done = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, related_name="user_todo", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
