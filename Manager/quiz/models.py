from django.db import models
from group.models import Group
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class QuizTest(models.Model):
    group = models.ForeignKey(
        Group, related_name="group_quiz", on_delete=models.CASCADE)
    quizname = models.CharField(max_length=150)
    description = models.CharField(max_length=300, blank=True, null=True)
    test_interval = models.IntegerField(null=True, blank=True)
    test_starttime = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.quizname


class UserQuizInfo(models.Model):
    quiz = models.ForeignKey(
        QuizTest, related_name='quiz_info', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_submitted = models.BooleanField(default=False)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"quiz- {self.quiz.quizname}- user {self.user}"


class Question(models.Model):
    qimage = models.ImageField(blank=True, upload_to='quiz/images/')
    quiz = models.ForeignKey(
        QuizTest, related_name='quiz_questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.IntegerField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(blank=True, max_length=200)
    option4 = models.CharField(blank=True, max_length=200)
    marks = models.IntegerField(default=1)
