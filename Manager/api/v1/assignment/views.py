import io

from api.v1.permissions import CreatorPermission, UserPermission
from rest_framework import decorators, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from assignment.models import (Assignment, AssignmentFiles, Response,
                               ResponseFiles)

from .serializers import (AssignmentFilesSerializer, AssignmentSerializer,
                          ResponseFilesSerializer, ResponseSerializer)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([CreatorPermission])
    def add_assignmentfiles(self, request, pk=None):
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)
        serializer = AssignmentFilesSerializer(data=data)
        if serializer.is_valid():
            assignment = self.get_object()
            serializer.save(assignment=assignment)
            return Response({"msg": "Assignment Files is added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([UserPermission])
    def add_response(self, request, pk=None):
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)
        serializer = ResponseSerializer(data=data)
        if serializer.is_valid():
            assignment = self.get_object()
            serializer.save(assignment=assignment, student=self.request.user)
            return Response({"msg": "Response is added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)


class AssignmentFilesViewSet(viewsets.ModelViewSet):
    queryset = AssignmentFiles.objects.all()
    serializer_class = AssignmentFilesSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([UserPermission])
    def add_responsefiles(self, request, pk=None):
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)
        serializer = ResponseFilesSerializer(data=data)
        if serializer.is_valid():
            response = self.get_object()
            serializer.save(response=response)
            return Response({"msg": "Responsecfiles is added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)


class ResponseFilesViewSet(viewsets.ModelViewSet):
    queryset = ResponseFiles.objects.all()
    serializer_class = ResponseFilesSerializer
