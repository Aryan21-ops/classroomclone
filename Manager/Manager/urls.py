"""Manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.v1.accounts.views import get_user_detail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get_user_detail/', get_user_detail, name='token_get_user_detail'),
    path('api/v1/', include("api.v1.urls")),
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', views.index, name="landing-page"),
    path('', include("group.urls", namespace="group")),
    path('quiz/', include("quiz.urls", namespace="quiz")),
    path('task/', include("assignment.urls", namespace="assignment")),
    path('post/', include("post.urls", namespace="post")),
    path('todo/', include("todo.urls", namespace="todo")),
    path('account/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
