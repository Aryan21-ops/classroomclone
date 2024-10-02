from rest_framework import viewsets
from api.v1.todo.serializers import TodoTasksSerializer
from todo.models import TodoTasks


class TodoViewSet(viewsets.ViewSet):
    queryset = TodoTasks.objects.all()
    serializer_class = TodoTasksSerializer
