from django.contrib import admin

# Register your models here.
from . import models






admin.site.register(models.Group)
admin.site.register(models.GroupMember)