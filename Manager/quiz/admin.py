from django.contrib import admin
from .models import QuizTest, Question, UserQuizInfo
# Register your models here.

admin.site.register(QuizTest)
admin.site.register(Question)
admin.site.register(UserQuizInfo)
