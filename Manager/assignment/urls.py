from django.urls import path
from .views import assignment_detail, create_assignment, update_assignment, delete, celery_test
app_name = 'assignment'

urlpatterns = [
    path('delete-assignment/<int:pk>/', delete, name='delete-assignment'),
    path('update-assignment/<int:pk>/',
         update_assignment, name='update-assignment'),
    path('create-assignment/<slug>/', create_assignment, name='create-assignment'),
    path('detail/<slug:assignment_slug>/', assignment_detail, name='assignment-detail'),
    path('celery/', celery_test, name='celery-test'),

]
