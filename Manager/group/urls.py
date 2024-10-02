from django.urls import path
from . import views
app_name = 'group'

urlpatterns = [
    path('classes/', views.ListGroup.as_view(), name="base1"),
    path('new/', views.CreateGroup.as_view(), name="create_group"),
    path('posts/in/<slug:slug>', views.SingleClass.as_view(), name="class_single"),
    path('join/<slug:slug>', views.JoinClass.as_view(), name="join"),
    path('leave/<slug:slug>', views.LeaveClass.as_view(), name="leave"),
    path('join_with_code/', views.Join, name="join-with-code"),

]
