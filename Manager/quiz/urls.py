from django.urls import path
from .views import *
app_name = 'quiz'

urlpatterns = [
    path('of/<slug:group_slug>/<int:quiz_id>/',
         quiz_question, name='quiztest'),
    path('create_quiz/<int:group_id>', create_quiz, name='create_quiz'),
    path('add-question/<int:quiz_id>', add_question, name='add_question'),
    path('update-question/<int:quiz_id>/<int:ques_id>',
         update_question, name='update_question'),
    path('api/<str:quizname>/', api_for_quiz, name='api_for_question'),
    path('api/<int:quiz_id>/marks/', api_for_quiz_mark, name='quiz_test_mark')
]
