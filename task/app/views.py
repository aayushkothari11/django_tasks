from django.shortcuts import render
from datetime import datetime
import psutil
import pytz
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from django.http.response import JsonResponse

# Create your views here.
def time(request):
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    return render(request, 'app/time.html', {'current_time':current_time})


def process(request):
    listOfProcessNames = list()
    for proc in psutil.process_iter():
       pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
       listOfProcessNames.append(pInfoDict)

    SortedListOfProcObjects = sorted(listOfProcessNames, key=lambda procObj: procObj['cpu_percent'], reverse=True)

    for elem in SortedListOfProcObjects:
        print(elem)

    top_10_processes = SortedListOfProcObjects[:10]

    return render(request, 'app/process.html', {'top_10_processes':top_10_processes})

@api_view(['PUT'])
def json(request):
    if request.method == "PUT":
        with open("app/data.txt", "a") as myfile:
            myfile.write("\n" + str(request.body))

        return JsonResponse({'message': 'Data dumped'}, status=status.HTTP_201_CREATED)
