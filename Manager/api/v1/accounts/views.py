from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import decorators
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class UserRegistrationViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@decorators.api_view(['get'])
@decorators.permission_classes([IsAuthenticated])
def get_user_detail(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)
