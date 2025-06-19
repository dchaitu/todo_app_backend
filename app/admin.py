from django.contrib import admin

from .models import Task, User

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ["task_id", "title", "user"]

admin.site.register(Task, TaskAdmin)


admin.site.register(User)