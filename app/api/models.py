from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ("DEVELOPER", "Developer"),
    ("ANALYST", "Analyst")
)


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
class Iteration(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default="DEVELOPER")

    def __str__(self):
        return self.name


class TaskItem(models.Model):
    iteration = models.ForeignKey(Iteration, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    isDevelopment = models.BooleanField(default=False)
    isAnalyze = models.BooleanField(default=False)
    isTest = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.task.title


class EffortItem(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    effort = models.FloatField(null=True)

    class Meta:
        unique_together = ('task_item', 'member')

    def __str__(self):
        return self.task_item.task.title + "-" + self.member.name + "-" + str(self.effort)
