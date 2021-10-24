from django.db import models
from django.contrib.auth.models import User

class TaskEntry(models.Model):
    CATIGORY_CHOICES = [ ('HO', 'Home'), ('SC','School'), ('WO','Work'), ('SI','Self Improvement'), ('OT', 'Other')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    catigory = models.CharField(max_length=2, choices=CATIGORY_CHOICES, default='OT')
    complete = models.BooleanField()
