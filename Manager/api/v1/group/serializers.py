from rest_framework import serializers
from group.models import Group, GroupMember
from django.contrib.auth import get_user_model
from api.v1.post.serializers import PostSerializer
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UsernameField(serializers.Field):
    # def get_attribute(self, instance):
    #     # We pass the object instance onto `to_representation`,
    #     # not just the field attribute.
    #     return instance

    def to_representation(self, value):

        return value.username


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UsernameField(read_only=True)

    class Meta:
        model = GroupMember
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    creator = UsernameField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
