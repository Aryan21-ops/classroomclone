from rest_framework import viewsets, decorators, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from assignment.tasks import add_assignment_in_post

from .serializers import GroupSerializer, GroupMemberSerializer
from api.v1.post.serializers import PostSerializer
from api.v1.quiz.serializers import QuizTestSerializer
from api.v1.assignment.serializers import AssignmentSerializer, AssignmentFilesSerializer

from api.v1.permissions import UserPermission, CreatorPermission

from group.models import Group, GroupMember
from django.db.models import Q
import json


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = Group.objects.filter(
            Q(members=self.request.user.id) | Q(creator=self.request.user.id)).distinct()
        return queryset

    @action(detail=True, methods=['get'])
    def get_post_list(self, request, pk=None):
        obj = self.get_object()
        data = obj.group_posts.all().order_by('-created_at')
        list = PostSerializer(data, many=True)
        return Response(list.data)

    @action(detail=True, methods=['get'])
    def get_quiz_list(self, request, pk=None):
        obj = self.get_object()
        data = obj.group_quiz.all()
        list = QuizTestSerializer(data, many=True)
        return Response(list.data)

    @action(detail=True, methods=['get'])
    def get_assignment_list(self, request, pk=None):
        obj = self.get_object()
        data = obj.group_assignment.all().order_by('-task_created')
        list = AssignmentSerializer(data, many=True)
        return Response(list.data)

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([UserPermission])
    def addposts(self, request, pk=None):
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            group = self.get_object()
            user = self.request.user
            serializer.save(user=user, group=group)
            return Response({"msg": "post is added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([CreatorPermission])
    def createQuiz(self, request, pk=None):
        data = request.data
        serializer = QuizTestSerializer(data=data)
        if serializer.is_valid():
            group = self.get_object()
            serializer.save(group=group)
            return Response({"msg": "Quiz is created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([CreatorPermission])
    def add_assignment(self, request, pk=None):
        data = request.data

        serializer = AssignmentSerializer(data=data)
        print(serializer.initial_data)
        if serializer.is_valid():
            group = self.get_object()
            assignment = serializer.save(group=group)
            print(assignment)
            add_assignment_in_post.delay(
                group_id=group.id, user_id=self.request.user.id, assignment_id=assignment.id)
            return Response({"msg": "Assignment is created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GroupMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
