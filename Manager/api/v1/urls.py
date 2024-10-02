from rest_framework import routers
from rest_framework.routers import DefaultRouter

from api.v1.accounts.views import UserRegistrationViewSet
from api.v1.assignment.views import AssignmentViewSet, AssignmentFilesViewSet, ResponseViewSet, ResponseFilesViewSet
from api.v1.post.views import PostViewSet
from api.v1.group.views import GroupViewSet, GroupMemberViewSet
from api.v1.quiz.views import QuizTestViewSet, UserQuizInfoViewSet, QuestionViewSet
from api.v1.todo.views import TodoViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'group', GroupViewSet)
router.register(r'groupmembers', GroupMemberViewSet)
router.register(r'quiz', QuizTestViewSet)
router.register(r'quiz_info', UserQuizInfoViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'assignment', AssignmentViewSet)
router.register(r'assignment_files', AssignmentFilesViewSet)
router.register(r'response', ResponseViewSet)
router.register(r'response_files', ResponseFilesViewSet)
router.register(r'user', UserRegistrationViewSet, basename='user-registration')
router.register(r'todo', TodoViewSet)


urlpatterns = []
urlpatterns += router.urls
