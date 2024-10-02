from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
import json
from .models import *
from .forms import QuizForm, QuestionForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import messages


@csrf_exempt
def api_for_quiz(request, quizname):
    try:

        quiz = QuizTest.objects.filter(quizname=quizname).first()
        questions = Question.objects.filter(quiz=quiz)
        questions_set = []
        for i in questions:
            question = {}
            question['question_id'] = i.id
            question['question'] = i.question
            question['answer'] = i.answer
            options = []
            options.append(i.option1)
            options.append(i.option2)
            if len(i.option3) > 0:
                options.append(i.option3)
            if len(i.option4) > 0:
                options.append(i.option4)
            question['options'] = options
            questions_set.append(question)
        return JsonResponse(questions_set, safe=False)
    except QuizTest.DoesNotExist:
        return JsonResponse({'msg': 'quiz not found'})


@csrf_exempt
def api_for_quiz_mark(request, quiz_id):
    data = json.loads(request.body)
    try:
        quiz = QuizTest.objects.get(id=quiz_id)
        total_mark = 0
        print(data)

        sol = data['solutions']

        for i in range(0, len(sol)):
            question = Question.objects.get(id=sol[i]['question_id'])
            x = int(sol[i]['user_response']) + 1

            if question.answer == x:
                total_mark += question.marks

        user = User.objects.filter(username=data['user']).first()
        group = Group.objects.get(id=data['group_id'])

        if user is not group.creator and user in group.members.all():
            userinfo = UserQuizInfo.objects.create(
                mark=total_mark, user_submitted=True)
            userinfo.quiz = quiz
            userinfo.user = user
            userinfo.save()
            return JsonResponse({'msg': 'successfully posted', 'marks': total_mark})
        else:
            return JsonResponse({'msg': 'u cannot participate in the quiz', 'marks': total_mark})
    except:
        return JsonResponse({'msg': 'something went wrong'})


def quiz_question(request, quiz_id, group_slug):
    quiz = QuizTest.objects.get(id=quiz_id)
    group = Group.objects.filter(slug=group_slug).first()
    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'group': group})


def add_question(request, quiz_id):
    quiz = QuizTest.objects.get(id=quiz_id)

    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        marks = request.POST.get('marks')
        if answer not in range(1, 5):
            return JsonResponse({'msg': 'Invalid answer!!!', 'code': '2'})
        quiz_id = request.POST.get('quiz_id')
        quiz1 = QuizTest.objects.get(id=quiz_id)
        qObject = Question.objects.create(
            question=question, answer=answer, option1=option1, option2=option2, option3=option3, option4=option4, marks=marks, quiz=quiz1)

        qObject.quiz = quiz1
        qObject.save()
        return JsonResponse({'msg': 'question added successfully'})
    context = {
        'questionform': QuestionForm,
        'quiz': quiz,
    }

    return render(request, 'quiz/add-question-page.html', context)


def create_quiz(request, group_id):
    group = Group.objects.get(id=group_id)
    form = QuizForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.group = group
        instance.save()
        return redirect('quiz:add_question', quiz_id=instance.id)
    return reverse('group:class_single', kwargs={'slug': group.slug})


def update_question(request, quiz_id, ques_id):
    quiz = QuizTest.objects.get(id=quiz_id)
    instance = Question.objects.get(id=ques_id)
    form = QuestionForm(request.POST or None, instance=instance)
    slug = quiz.group.slug

    if form.is_valid():
        form.save()
        messages.success(request, "Question updated")
        return redirect('quiz:quiztest', quiz_id=quiz.id, group_slug=slug)
    return render(request, 'add-question-page.html', {'form': form})
