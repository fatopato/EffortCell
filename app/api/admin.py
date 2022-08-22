from django.contrib import admin
from .models import Member, TaskItem, Task, EffortItem, Iteration
# Register your models here.
admin.site.register(Member)
admin.site.register(TaskItem)
admin.site.register(Task)
admin.site.register(EffortItem)
admin.site.register(Iteration)
