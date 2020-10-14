from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('time/', views.time, name='time'),
    path('process/',views.process, name='process'),
    path('json/',views.json, name='json'),
]
