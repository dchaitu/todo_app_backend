from enum import Enum
from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser


class TaskStatus(Enum):

    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in progress"
    DONE = "done"
    CANCELED = "canceled"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)

class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    @classmethod
    def choices(cls):
        return tuple((i.value.lower(), i.name) for i in cls)

# Create your models here.
class Task(models.Model):
    task_id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=150, default=None, blank=True, null=True)
    label = models.CharField(max_length=50, default=None, blank=True, null=True)
    status = models.CharField(max_length=20,choices=TaskStatus.choices(), default=TaskStatus.TODO)
    priority = models.CharField(max_length=20,choices=TaskPriority.choices(),default=TaskPriority.MEDIUM)
    user = models.ForeignKey('User',on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    picture = models.CharField(max_length=200, default="https://ui.shadcn.com/avatars/03.png")
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)