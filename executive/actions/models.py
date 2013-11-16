from django.db import models
from json_field import JSONField

class Project(models.Model):
    name = models.CharField(max_length=1000)
    parent = models.ForeignKey('self')

    def get_parent(self):
        if hasattr(self, 'parent') and self.__class__.objects.filter(pk = self.parent.id).exists():
            return self.parent

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
