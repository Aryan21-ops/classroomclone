
from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from post.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = StringRelatedField(read_only=True)
    comments_count = serializers.SerializerMethodField()
    comment_list = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Post
        fields = ['group', 'user', 'created_at',
                  'message', 'comments_count', 'comment_list']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_comment_list(self, obj):
        data = obj.comments.all().order_by('-created_at')
        list = CommentSerializer(data, many=True)
        return list.data
