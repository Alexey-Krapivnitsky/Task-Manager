from django.urls import path
from taskapp.views import TasksCreateView, TasksFilterView, ChangeTaskView, UpdateTaskView

app_name = 'taskapp'

urlpatterns = [
    path('tasks/', TasksCreateView.as_view(), name='tasks'),
    path('task_filter/', TasksFilterView.as_view()),
    path('task_change/', ChangeTaskView.as_view()),
    path('task_update/<int:pk>/', UpdateTaskView.as_view(), name='task_update'),
]