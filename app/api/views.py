from .models import Task, TaskItem, EffortItem, Member, Iteration
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from bootstrap_modal_forms.generic import BSModalCreateView
from django.urls import reverse_lazy

from .forms import IterationForm, MemberForm


class IterationListView(ListView):
    model = Iteration


@method_decorator(login_required, name='dispatch')
class IterationCreateView(CreateView):
    model = Iteration
    template_name = 'api/iteration_edit.html'
    form_class = IterationForm

    def get_success_url(self):
        return reverse('iterations')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(IterationCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class IterationUpdateView(UpdateView):
    model = Iteration
    template_name = 'api/iteration_edit.html'
    form_class = IterationForm

    def get_success_url(self):
        return reverse('iterations')


class TaskItemList(ListView):
    model = TaskItem


@method_decorator(login_required, name='dispatch')
class MemberCreateView(CreateView):
    model = Member
    fields = ('name', 'role')
    template_name = 'api/member_edit.html'

    def get_success_url(self):
        return reverse('members')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(MemberCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class MemberUpdateView(UpdateView):
    model = Member
    fields = ('name', 'role')
    template_name = "api/member_edit.html"

    def get_success_url(self):
        return reverse('members')


@method_decorator(login_required, name='dispatch')
class MemberListView(ListView):
    model = Member
    template_name = "member_list.html"


def dashboard(request, pk):
    iteration = Iteration.objects.get(pk=pk)
    task_items = TaskItem.objects.filter(iteration__pk=pk)
    effort_counts = {}
    effort_counts_pk = {}
    all_members = Member.objects.all()
    for member in all_members:
        total_effort = get_total_member_effort(task_items, member.pk)
        print(member.pk, ": ", total_effort)
        effort_counts[member.name] = [total_effort, member.pk]
        effort_counts_pk[member.pk] = total_effort

    print(effort_counts)
    return render(request, "api/dashboard.html"
                  , {'task_items': task_items, 'iteration': iteration,
                     'effort_counts': effort_counts, 'effort_counts_pk': effort_counts_pk})


def add_to_task_item(request, task_item_pk, member_pk, effort):
    task_item = TaskItem.objects.get(pk=task_item_pk)
    member = Member.objects.get(pk=member_pk)
    effort_item = EffortItem()
    effort_item.member = member
    effort_item.task_item = task_item
    effort_item.effort = effort
    effort_item.save()

    return redirect("dashboard", task_item.iteration.pk)


def update_effort(request, effort_pk, effort_val):
    effort_item = get_object_or_404(EffortItem, pk=effort_pk)
    effort_item.effort = effort_val
    return redirect("dashboard", effort_item.task_item.iteration.pk)


class EffortItemDeleteView(DeleteView):
    model = EffortItem

    def get_success_url(self):
        return redirect(self.request.META.get('HTTP_REFERER'))


class MemberCreateView2(BSModalCreateView):
    template_name = 'api/create_member.html'
    form_class = MemberForm
    success_message = 'Success: Member was created.'
    success_url = reverse_lazy('members')


def get_total_member_effort(taskitem_qs, member_pk):
    return sum([effort_item.effort for task_item in taskitem_qs for effort_item in task_item.effortitem_set.all() if
                effort_item.member.pk == member_pk])
