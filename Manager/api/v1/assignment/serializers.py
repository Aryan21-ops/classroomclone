from rest_framework import serializers
from assignment.models import Assignment, AssignmentFiles, Response, ResponseFiles
from django.contrib.auth import get_user_model
User = get_user_model()


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment

        exclude = ('slug',)


class AssignmentFilesSerializer(serializers.ModelSerializer):
    attachments = serializers.FileField(allow_empty_file=True)

    class Meta:
        model = AssignmentFiles
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Response
        fields = '__all__'


class ResponseFilesSerializer(serializers.ModelSerializer):
    rfiles = serializers.FileField(allow_empty_file=True)

    class Meta:
        model = ResponseFiles
        fields = '__all__'
