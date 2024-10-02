from rest_framework import serializers
from todo.models import TodoTasks
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoTasksSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoTasks
        fields = ('__all__')
