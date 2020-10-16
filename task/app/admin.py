from django.contrib import admin
from .models import Time, Process

'''
To view the models and their data in the Django Admin Panel.
'''
admin.site.register(Time)
admin.site.register(Process)
