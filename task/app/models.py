from django.db import models
import datetime
from django.utils.timezone import now

class Time(models.Model):
    last_visited = models.DateTimeField(default=now, blank=True)
