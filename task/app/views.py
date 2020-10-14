from django.shortcuts import render
import datetime
import psutil
import pytz
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from .models import *

# Create your views here.
def time(request):
    time_now = datetime.datetime.now(datetime.timezone.utc)
    print(time_now)
    current_time = time_now.strftime("%H:%M:%S")

    time = Time.objects.all()[0]
    last_visited = time.last_visited
    time.last_visited = time_now
    time.save()
    print(time.last_visited)

    print("Current Time =", current_time)
    # FMT = '%H:%M:%S'
    # last_visited = last_visited.strftime("%H:%M:%S")
    # difference = datetime.datetime.strptime(current_time, FMT) - datetime.datetime.strptime(str(last_visited), FMT)

    difference = time_now - last_visited

    last_visited = last_visited.strftime("%H:%M:%S")

    return render(request, 'app/time.html', {'current_time':current_time,'last_visited':last_visited,'difference':difference})




def process(request):
    listOfProcessNames = list()
    for proc in psutil.process_iter():
       pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
       listOfProcessNames.append(pInfoDict)

    SortedListOfProcObjects = sorted(listOfProcessNames, key=lambda procObj: procObj['cpu_percent'], reverse=True)

    for elem in SortedListOfProcObjects:
        if len(Process.objects.filter(pid=elem['pid']))==1:
            process = Process.objects.get(pid=elem['pid'])
            current_diff = elem['cpu_percent'] - float(process.cpu_usage)
            process.difference_from_last_time = current_diff
            process.cpu_usage = elem['cpu_percent']
            process.save()
        elif len(Process.objects.filter(pid=elem['pid']))==0:
           process = Process.objects.create(pid=elem['pid'],name=elem['name'],cpu_usage=elem['cpu_percent'],difference_from_last_time=0)
           process.save()

    top_10_processes = Process.objects.all().order_by('-cpu_usage')[:10]

    return render(request, 'app/process.html', {'top_10_processes':top_10_processes})



@api_view(['PUT'])
def json(request):
    if request.method == "PUT":
        with open("app/data.txt", "a") as myfile:
            myfile.write("\n" + str(request.body))

        return JsonResponse({'message': 'Data dumped'}, status=status.HTTP_201_CREATED)
