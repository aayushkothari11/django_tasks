from django.shortcuts import render
import datetime
import psutil
import pytz
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse
from .models import *

'''
Function that converts time from UTC to local

Input - UTX datatime
Output - local datetime
'''
def utc_to_local(utc_dt):
    tz = pytz.timezone('Asia/Kolkata')
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=tz)


'''
A function which gets the current time and stores it in the database.
The time value already present in the database before updation is used to calculate the differnce in values.

Input - NA
Output - A dictionary of current time, last visited and difference is passed to the template.
'''
def time(request):
    time_now_utc = datetime.datetime.now(datetime.timezone.utc)
    local_datetime_now = utc_to_local(time_now_utc)
    current_time_local = local_datetime_now.strftime("%H:%M:%S")
    print("Current Time =", current_time_local)

    time = Time.objects.all()[0]
    last_visited_utc = time.last_visited
    time.last_visited = time_now_utc
    time.save()

    last_visited_local_datetime = utc_to_local(last_visited_utc)
    last_visited_local_time = last_visited_local_datetime.strftime("%H:%M:%S")
    print("Last visited Time =", last_visited_local_time)


    # FMT = '%H:%M:%S'
    # last_visited = last_visited.strftime("%H:%M:%S")
    # difference = datetime.datetime.strptime(current_time, FMT) - datetime.datetime.strptime(str(last_visited), FMT)

    difference = time_now_utc - last_visited_utc

    return render(request, 'app/time.html', {'current_time':current_time_local,'last_visited':last_visited_local_time,'difference':difference})


'''
A function which uses the psutil package to get information about the processes running at that moment.
The processes are then stored in the database with pid as primary key if they are not present with a difference value of zero.
If the process are already present in the database then value of diffence is updated.

Input - NA
Output - A dictionary of top 10 processes sorted on CPU usage is passed to the template
'''

def process(request):
    '''
    Get all the running processes and store important properties such as pid, name and cpu_percent in a list of dictionaries.
    '''
    list_of_process_names = list()
    for proc in psutil.process_iter():
       process_info_dict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
       list_of_process_names.append(process_info_dict)

    '''
    Sort the list based on the CPU percentages.
    '''
    sorted_list_of_process_objects = sorted(list_of_process_names, key=lambda proc_obj: proc_obj['cpu_percent'], reverse=True)


    '''
    Create a new Process object if pid not present in the database with a differnce of zero.
    If pid already present update the differnce value accordingly.
    '''
    for elem in sorted_list_of_process_objects:
        if len(Process.objects.filter(pid=elem['pid']))==1:
            process = Process.objects.get(pid=elem['pid'])
            current_diff = elem['cpu_percent'] - float(process.cpu_usage)
            process.difference_from_last_time = current_diff
            process.cpu_usage = elem['cpu_percent']
            process.save()
        elif len(Process.objects.filter(pid=elem['pid']))==0:
           process = Process.objects.create(pid=elem['pid'],name=elem['name'],cpu_usage=elem['cpu_percent'],difference_from_last_time=0)
           process.save()

    '''
    Get a list of the top 10 processes in the database sorted on the cpu percent value.
    '''
    top_10_processes = Process.objects.all().order_by('-cpu_usage')[:10]

    return render(request, 'app/process.html', {'top_10_processes':top_10_processes})


'''
An API which is exposed only to the PUT method. The API takes in the JSON passed in the request body and dumps it in the local text file.
Accordingly a JSON Response is passed if the operation was successful.

Input - JSON body
Output - Data dumped in the local text file
'''
@api_view(['PUT'])
def json(request):
    if request.method == "PUT":
        with open("app/data.txt", "a") as myfile:
            myfile.write("\n" + str(request.body))

        return JsonResponse({'message': 'Data dumped'}, status=status.HTTP_201_CREATED)
