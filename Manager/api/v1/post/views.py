from rest_framework import viewsets, permissions, status, decorators
from api.v1.post.serializers import PostSerializer, CommentSerializer
from post.models import Comment, Post
from group.models import GroupMember, Group
from rest_framework.decorators import action
from rest_framework.response import Response
import io
from rest_framework.parsers import JSONParser
from api.v1.permissions import UserPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = UserPermission

    @action(detail=True, methods=['post'])
    @decorators.permission_classes([UserPermission])
    def addcomments(self, request):
        stream = io.BytesIO(request.data)
        data = JSONParser().parse(stream)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            user = self.request.user
            post = self.get_object()
            serializer.save(user=user, post=post)
            return Response({"msg": "comment is added"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg": "data is not valid"}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def deletecomment(self, request):
        id = request.data.get('id')
        try:
            comment = Comment.objects.get(id=id)
            comment.delete()
            return Response({'msg': 'Comment deleted'}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'msg': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)
