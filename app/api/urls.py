from django.urls import path
from .views import IterationListView, TaskItemList, dashboard, add_to_task_item, MemberCreateView\
    , MemberListView, MemberUpdateView, IterationUpdateView, IterationCreateView

urlpatterns = [
    path('iterations/', IterationListView.as_view(), name='iterations'),
    path('iteration-create/', IterationCreateView.as_view(), name='iteration_create'),
    path('iteration-update/<pk>/', IterationUpdateView.as_view(), name='iteration_update'),
    path('taskitems/', TaskItemList.as_view(), name='taskitems'),
    path('dashboard/<pk>', dashboard, name='dashboard'),
    path('add_to_task_item/<task_item_pk>/<member_pk>/<effort>', add_to_task_item, name='add_to_task_item'),
    path('member-create/', MemberCreateView.as_view(), name='member_create'),
    path('member-update/<pk>/', MemberUpdateView.as_view(), name='member_update'),
    path('members/', MemberListView.as_view(), name='members'),
]