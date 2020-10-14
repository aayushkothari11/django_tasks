from django.db import models
import datetime
from django.utils.timezone import now

class Time(models.Model):
    last_visited = models.DateTimeField(default=now, blank=True)

class Process(models.Model):
    pid = models.CharField(max_length=10, primary_key = True)
    cpu_usage = models.DecimalField(max_digits=10, decimal_places=5)
    name = models.CharField(max_length=100)
    difference_from_last_time = models.DecimalField(max_digits=10, decimal_places=5)
