from django.contrib import admin
from tasks.models import TaskEntry
from tasks.models import TaskCategory

# Register your models here.
admin.site.register(TaskEntry)
admin.site.register(TaskCategory)
