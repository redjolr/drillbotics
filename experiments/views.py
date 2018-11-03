from django.shortcuts import render
from django.http import HttpResponse
from .models import Experiment, Measurement
import json

def allexperiments(request):

    return render(request, 'experiments/allexperiments.html')

def experiment_data(request, id, sensor_id):
    downsample_val = float(request.GET['downsample'])   #ranges from 0 to 1
    total_points = int(request.GET['total_points'])     #total points of the experiment. Instead of accesing the database again, we get it from the client
    sensor_id = int(sensor_id)
    data = Measurement.objects.values("time_micro", "value").filter(experiment_id=id, sensor_id=sensor_id).order_by('time_micro')

    rock_set = Experiment.objects.filter(id=id).select_related('rock_id').values('rock_id', 'rock_id__name')

    rock = {'id': rock_set[0]['rock_id'], 'name':rock_set[0]['rock_id__name']}

    downsample_step = int(1/downsample_val)
    time_arr = [measurement['time_micro'] for measurement in data[0::downsample_step] ]
    value_arr = [measurement['value'] for measurement in data[0::downsample_step]]

    return HttpResponse(json.dumps({'rock': rock,'data':{'time': time_arr, 'values':value_arr,}}))
