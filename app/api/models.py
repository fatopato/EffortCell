import datetime

from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ("DEVELOPER", "Developer"),
    ("ANALYST", "Analyst")
)


class AbstractBaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


# Create your models here.
class Task(AbstractBaseModel):
    title = models.CharField(max_length=100, null=True, blank=True)

    # def __str__(self):
    #     return self.title


class Iteration(AbstractBaseModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def is_active(self):
        return datetime.date.today() <= self.end_date and datetime.date.today() >= self.start_date

    @property
    def total_effort(self):
        return sum([effort_item.effort for task_item in self.taskitem_set.all() for effort_item in
                    task_item.effortitem_set.all()])
    @property
    def total_issues(self):
        return len(self.taskitem_set.all())

    # def __str__(self):
    #     return self.title


class Member(AbstractBaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default="DEVELOPER")

    # def __str__(self):
    #     return self.name


class TaskItem(AbstractBaseModel):
    previous = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name='advance', blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name='child', blank=True)
    iteration = models.ForeignKey(Iteration, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    isDevelopment = models.BooleanField(default=False)
    isAnalyze = models.BooleanField(default=False)
    isTest = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.title


class EffortItem(AbstractBaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE)
    effort = models.FloatField(null=True)

    class Meta:
        unique_together = ('task_item', 'member')

    @property
    def members_total_effort(self):
        task_items = TaskItem.objects.filter(iteration__pk=self.task_item.iteration.pk, member__pk=member_pk)
        return sum([effort_item.effort for task_item in task_items for effort_item in task_item.effortitem_set.all()])

    # def __str__(self):
    #     return self.task_item.title + "-" + self.member.name + "-" + str(self.effort)
