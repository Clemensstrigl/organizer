from django.db import models
from django.contrib.auth.models import User

class TaskCategory(models.Model):
    category = models.CharField(max_length=128)
    def __str__(self):
        return self.category

class TaskEntry(models.Model):
    CATIGORY_CHOICES = [ ('HO', 'Home'), ('SC','School'), ('WO','Work'), ('SI','Self Improvement'), ('OT', 'Other')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    complete = models.BooleanField()
