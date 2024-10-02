# from __future__ import absolute_import

# from celery import shared_task
# from celery.decorators import task
# from django.contrib.auth import get_user_model
# from group.models import Group
# from post.models import Post

# from assignment.models import Assignment

# User = get_user_model()


# @shared_task
# def test(param):
#     return 'The tasks executed with the following parameter: "%s" '


# @task(name="add_assignment_in_post")
# def add_assignment_in_post(user_id, assignment_id, group_id):
#     group = Group.objects.get(id=group_id)
#     assignment = Assignment.objects.values('title').get(id=assignment_id)
#     user = User.objects.get(id=user_id)
#     post = Post.objects.create(user=user, group=group)
#     post.message = assignment.title
#     post.save()
#     print(post.message)
