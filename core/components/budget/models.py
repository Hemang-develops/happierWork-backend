from django.db import models
from django.utils import timezone

class BudgetData(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    designation = models.CharField(max_length=18)
    department = models.CharField(max_length=11)
    budget = models.IntegerField()
    location = models.CharField(max_length=9)
    lastUpdated0 = models.CharField(max_length=12, default='Not Updated')
    lastUpdated1 = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id  # or any other string representation
