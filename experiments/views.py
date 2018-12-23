from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import connection
from .models import Experiment, Measurement
from sensors.models import Sensor
import matplotlib.pyplot as plt
import json

@login_required(login_url='/login/')
def allexperiments(request):
    experiments = Experiment.objects.raw('''
                    SELECT experiment.id, to_char( start_time, 'DD Month YYYY') as date,
            	   to_char( start_time, 'HH24:MI:SS') as starting_time,
            	   (subquery.duration::text)::interval,
            	   rock.name as rock_name,
            	   subquery.total_points/subquery.nr_of_sensors as nr_of_samples,
            	   subquery.total_points/subquery.nr_of_sensors/subquery.duration as frequency,
            	   subquery.nr_of_sensors
            FROM experiment
            INNER JOIN rock on experiment.rock_id = rock.id
            INNER JOIN
            (
            	SELECT experiment_id, COUNT(*) as total_points, MAX(time_micro)/1000000 as duration,
            		   MAX(sensor_id) as nr_of_sensors
            	FROM measurement
            	GROUP BY experiment_id
            ) subquery ON subquery.experiment_id = experiment.id
            ORDER BY start_time DESC;
    ''')
    return render(request, 'experiments/allexperiments.html', {'experiments':experiments})

@login_required(login_url='/login/')
def experiment_data(request, id):
    downsample_val = float(request.GET['downsample'])   #ranges from 0 to 1
    total_points = int(request.GET['total_points'])     #total points of the experiment. Instead of accesing the database again, we get it from the client
    sensors =request.GET['sensors'].split("_")



    data = Measurement.objects.values("time_micro", "value", "sensor_id", "sensor_id__name").filter(experiment_id=id, sensor_id__in=sensors).order_by('sensor_id', 'time_micro')

    rock_set = Experiment.objects.filter(id=id).select_related('rock_id').values('rock_id', 'rock_id__name')
    rock = {'id': rock_set[0]['rock_id'], 'name':rock_set[0]['rock_id__name']}

    sensors_data = []
    downsample_step = int(1/downsample_val)

    per_sensor_datalength = int(len(data)/len(sensors))
    time_arr = [int(measurement['time_micro']/1000000) for measurement in data[0:per_sensor_datalength:downsample_step]]


    # print("YOO", data)
    for i  in range(len(sensors)):
        sensor_id = data[i*per_sensor_datalength]['sensor_id']
        sensor_name = data[i*per_sensor_datalength]['sensor_id__name']
        sensors_data.append({"sensor_name":sensor_name, "values": [measurement['value'] for measurement in data[i*per_sensor_datalength:i*per_sensor_datalength+per_sensor_datalength:downsample_step]] } )


    #matplotlib
    fig = plt.figure()
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')
    fig.savefig('graph.png')
    #matplotlib


    return HttpResponse(json.dumps({'rock': rock,'data':{'time': time_arr, 'sensors':sensors_data}}))

@login_required(login_url='/login/')
def download_dataset(request, experiment_id):
    response = HttpResponse()
    sensors = list(Sensor.objects.values('abbreviation').all().order_by('id'))
    experiment = Experiment.objects.values('start_time').filter(id=experiment_id)
    exp_date = experiment[0]['start_time'].strftime( "%d-%B-%Y")
    data = Measurement.objects.values('time_micro', 'value', 'sensor_id').filter(experiment_id=experiment_id).order_by('time_micro', 'sensor_id')


    columns = "time_micro"
    for sensor in sensors:
        columns+= ","+sensor['abbreviation']
    response.write(columns+"\n")

    row = ''
    i=0
    for measurement in data:
        if i==0:
            row +=str(measurement['time_micro'])+','+str(measurement['value'])
        else:
            row += ','+str(measurement['value'])
        i+=1
        if i==len(sensors):
            response.write(row+"\n")
            row=''
            i=0

    filename = "Experiment_"+exp_date+".csv"

    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response
