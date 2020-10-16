from django.db import models
import datetime
from django.utils.timezone import now

'''
A Time model which stores the time the user last visited the site as a DateTimeField with default equal to the UTC timezone current time.
'''
class Time(models.Model):
    last_visited = models.DateTimeField(default=now, blank=True)

'''
A Process model which stores information about the process such as process id, current CPU usage, Name of the Process and the difference in CPU usage from the last time the url was called.
'''
class Process(models.Model):
    pid = models.CharField(max_length=10, primary_key = True)
    cpu_usage = models.DecimalField(max_digits=10, decimal_places=5)
    name = models.CharField(max_length=100)
    difference_from_last_time = models.DecimalField(max_digits=10, decimal_places=5)
