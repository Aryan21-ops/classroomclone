# from celery.decorators import task
# from assignment.models import Assignment
# from group.models import Group, GroupMember
# from .models import TodoTasks


# @task(name="update_task_to_group_members")
# def update_task_to_group_members(assignment_id, group_id):
#     assignment = Assignment.objects.get(id=assignment_id)
#     group_id = assignment.group.id
#     group = Group.objects.get(id=group_id)
#     msg = f'{group.name} - {assignment.title}'
#     for member in group.members.all():
#         TodoTasks.objects.create(
#             user=member, title=msg, deadline=assignment.deadline)
