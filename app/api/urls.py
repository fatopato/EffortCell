from django.urls import path
from .views import IterationListView, TaskItemList, dashboard

urlpatterns = [
    path('iterations/', IterationListView.as_view(), name='iterations'),
    path('taskitems/', TaskItemList.as_view(), name='taskitems'),
    path('dashboard/<pk>', dashboard, name='dashboard'),
]