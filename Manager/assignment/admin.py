from django.contrib import admin
from .models import Assignment, Response, AssignmentFiles, ResponseFiles
# Register your models here.


class AssignmentFilesAdmin(admin.StackedInline):
    model = AssignmentFiles


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    inlines = [AssignmentFilesAdmin]

    class Meta:
        model = Assignment


class ResponseFilesAdmin(admin.StackedInline):
    model = ResponseFiles


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    inlines = [ResponseFilesAdmin]

    class Meta:
        model = Response
