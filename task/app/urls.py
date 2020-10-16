from django.urls import path
from . import views

app_name = 'app'

'''
The route 'time/' calls the time function which displays the current time and difference in time from the last visit.
The route 'process/' calls the process function which displays the top 10 process information sorted on CPU usage.
The route 'json/' is an API to dump Json body in a local text file.
'''
urlpatterns = [
    path('time/', views.time, name='time'),
    path('process/',views.process, name='process'),
    path('json/',views.json, name='json'),
]
