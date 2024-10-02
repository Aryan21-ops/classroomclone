from rest_framework import viewsets, status, decorators
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.quiz.serializers import UserQuizInfoSerializer, QuestionSerializer, QuizTestSerializer
from quiz.models import UserQuizInfo, QuizTest, Question
from api.v1.permissions import UserPermission, CreatorPermission

from rest_framework.parsers import JSONParser
import io


class QuizTestViewSet(viewsets.ModelViewSet):
    queryset = QuizTest.objects.all()
    serializer_class = QuizTestSerializer

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([CreatorPermission])
    def createQuestion(self, request, pk=None):
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            quiz = self.get_object()
            serializer.save(quiz=quiz)
            return Response({"msg": "Question has been added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    @decorators.permission_classes([CreatorPermission])
    def quiz_test_mark(self, request, pk=None):
        obj = self.get_object()
        all_quiz_info = obj.quiz_info.all()
        serializer = UserQuizInfoSerializer(all_quiz_info, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    @decorators.permission_classes([CreatorPermission])
    def questions_list(self, request, pk=None):
        obj = self.get_object()
        questions_list = obj.quiz_questions.all()
        serializer = QuestionSerializer(questions_list, many=True)
        return Response(serializer.data)


class UserQuizInfoViewSet(viewsets.ModelViewSet):
    queryset = UserQuizInfo.objects.all()
    serializer_class = UserQuizInfoSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
