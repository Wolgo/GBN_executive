from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=1000)
    parent = models.ForeignKey('self', null=True)

class Action(models.Model):
    name = models.CharField(max_length = 1000)
    deadline = models.DateField()
    project = models.ForeignKey(Project, null=True)
    completed = models.BooleanField(default = False)
    context = models.CharField(max_length = 1000)

class ScheduledAction(models.Model):
    """Scheduled action have a period within which they are active."""
    name = models.CharField(max_length = 1000)
    cron = models.CharField(max_length = 50)
    lastcompleted = models.DateTimeField(null = True)
