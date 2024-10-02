from rest_framework import serializers
from quiz.models import QuizTest, UserQuizInfo, Question
from api.v1.group.serializers import GroupSerializer
import json


class UsernameField(serializers.Field):

    def to_representation(self, value):
        return value.username


class QuizTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizTest
        fields = '__all__'


class UserQuizInfoSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UsernameField()

    class Meta:
        model = UserQuizInfo
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    qimage = serializers.ImageField(allow_empty_file=True)
    option1 = serializers.CharField(write_only=True)
    option2 = serializers.CharField(write_only=True)
    option3 = serializers.CharField(write_only=True, required=False)
    option4 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(QuestionSerializer, self).to_representation(instance)
        options = []
        options.append(instance.option1)
        options.append(instance.option2)
        if len(instance.option3) > 0:
            options.append(instance.option3)
        if len(instance.option4) > 0:
            options.append(instance.option4)

        ret['options'] = options
        return ret
