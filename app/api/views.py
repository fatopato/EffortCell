from django.shortcuts import render
from .models import Task, TaskItem, EffortItem, Member, Iteration
from django.views.generic.list import ListView


class IterationListView(ListView):
    model = Iteration


class TaskItemList(ListView):
    model = TaskItem


def dashboard(request, pk):
    iteration = Iteration.objects.get(pk=pk)
    task_items = TaskItem.objects.filter(iteration__pk=pk)
    effort_counts = {}
    effort_counts_pk = {}
    all_members = Member.objects.all()
    for member in all_members:
        total_effort = get_total_member_effort(task_items, member.pk)
        effort_counts[member.name] = total_effort
        effort_counts_pk[member.pk] = total_effort

    print(effort_counts)
    return render(request, "api/dashboard.html"
                  , {'task_items': task_items, 'iteration': iteration,
                      'effort_counts': effort_counts, 'effort_counts_pk': effort_counts_pk})


def get_total_member_effort(taskitem_qs, member_pk):
    task_items = taskitem_qs.filter(effortitem__member__pk=member_pk)
    return sum([effort_item.effort for task_item in task_items for effort_item in task_item.effortitem_set.all()])