from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from taskapp.models import Task, TaskLogger
from taskapp.serializers import TaskCreateSerializer, TaskFilterSerializer, ChangeTaskSerializer, TaskUpdateSerializer


class TasksCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(task_owner=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(task_owner=user)


class TasksFilterView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskFilterSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        if request.method == 'POST':
            task_status = self.request.data['task_status']
            task_finished_date = self.request.data['task_finished_date']
            if task_status and task_finished_date:
                queryset = queryset.filter(task_owner=user,
                                           task_status=task_status,
                                           task_finished_date__lte=task_finished_date)
            elif not task_finished_date:
                queryset = queryset.filter(task_owner=user,
                                           task_status=task_status)
        else:
            queryset = queryset.filter(task_owner=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        response = self.list(request)
        return response


class ChangeTaskView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = ChangeTaskSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        if request.method == 'POST':
            task_name = self.request.data['task_name']
            queryset = queryset.filter(task_owner=user,
                                       task_name=task_name)
            pk = queryset[0].pk
            return HttpResponseRedirect(reverse('taskapp:task_update', kwargs={'pk': pk}))
        else:
            queryset = queryset.filter(task_owner=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        response = self.list(request)
        return response


class UpdateTaskView(RetrieveUpdateAPIView):
    pk = None
    new_task_data = None
    old_task_data = None
    now_changes = []
    task_changes = {}
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logs = TaskLogger.objects.filter(task_id=self.get_object())
        for obj in logs:
            self.task_changes.setdefault(f'{obj.created_at}', obj.task_changes)
        return Response({'task': serializer.data, 'changes': self.task_changes})

    def perform_update(self, serializer):
        self.old_task_data = self.get_object()
        serializer.update(self.get_object(), self.check_serializer_data(self.old_task_data, serializer.validated_data))
        self.new_task_data = serializer.validated_data
        self.create_log(self.old_task_data, self.new_task_data)
        if self.now_changes:
            serializer.save()

    def create_log(self, old_data, new_data):
        self.now_changes = []
        task = old_data
        created_at = now()
        if old_data.task_name != new_data['task_name'] and new_data['task_name']:
            self.now_changes.append(f"task_name: old - {old_data.task_name}, new - {new_data['task_name']}")
        if old_data.task_description != new_data['task_description'] and new_data['task_description']:
            self.now_changes.append(f"task_description: old - {old_data.task_description}, "
                                    f"new - {new_data['task_description']}")
        if old_data.task_status != new_data['task_status']:
            self.now_changes.append(f"task_status: old - {old_data.task_status}, new - {new_data['task_status']}")
        if old_data.task_finished_date != new_data['task_finished_date'] and new_data['task_finished_date']:
            self.now_changes.append(f"finished_date: old - {old_data.task_finished_date}, "
                                    f"new - {new_data['task_finished_date']}")
        if self.now_changes:
            task_changes = ', '.join(self.now_changes)
            new_log = TaskLogger()
            new_log.task = task
            new_log.task_name = new_data['task_name']
            new_log.task_changes = task_changes
            new_log.created_at = created_at
            new_log.save()

    @staticmethod
    def check_serializer_data(old_data, new_data):
        if not new_data['task_name']:
            new_data['task_name'] = old_data.task_name
        if not new_data['task_description']:
            new_data['task_description'] = old_data.task_description
        if not new_data['task_status']:
            new_data['task_status'] = old_data.task_status
        if not new_data['task_finished_date']:
            new_data['task_finished_date'] = old_data.task_finished_date
        return new_data

