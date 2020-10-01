from django.db import models
from django.db.models import CharField, ForeignKey, DateTimeField, DO_NOTHING
from django.utils.timezone import now

from authapp.models import User


class Task(models.Model):
    STATUSES = (
        ('N', 'New'),
        ('P', 'Planned'),
        ('W', 'Working'),
        ('F', 'Finished'),
    )

    task_name = CharField(max_length=25, null=True)
    task_description = CharField(max_length=250, null=True)
    created_at = DateTimeField(default=now())
    task_status = CharField(max_length=1, choices=STATUSES)
    task_finished_date = DateTimeField(null=True)
    task_owner = ForeignKey(
        User,
        on_delete=DO_NOTHING,
    )


class TaskLogger(models.Model):
    created_at = DateTimeField(default=now())
    task_changes = CharField(max_length=250, null=True)
    task_name = CharField(max_length=25, null=True)
    task = ForeignKey(
        Task,
        on_delete=DO_NOTHING,
    )

