from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, StreamingHttpResponse
from django.db import connection
from django.db.models import F
from .models import Experiment, Measurement
from rocks.models import Rock
from sensors.models import Sensor
import matplotlib.pyplot as plt
import uuid, json, time, os
from accounts.accounts_utils import user_changed_password
from datetime import datetime, timedelta


@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def allexperiments(request):
    experiments = Experiment.objects.all()
    for experiment in experiments:
        experiment.duration = str(timedelta(seconds=experiment.duration/(10**6)))
        experiment.uploaded = "{:.0%}".format((experiment.uploaded_data_points) / experiment.nr_data_points)
    return render(request, 'experiments/allexperiments.html', {'experiments':experiments})

def create_random_walk():
    x = np.random.choice([-1,1],size=100, replace=True) # Sample with replacement from (-1, 1)
    return np.cumsum(x) # Return the cumulative sum of the elements




@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def experiment_data(request, id):
    graphs_dir = "media/graphs/"
    downsample_val = int(request.GET['downsample'])
    sensors = [int(sensor) for sensor in request.GET['sensors'].split("_")]
    experiment = Experiment.objects.get(id=id)
    total_points = experiment.uploaded_data_points
    experiment_values=Experiment.objects.filter(id=id).values('description', 'duration', 'nr_data_points', 'sampling_freq')[0]
    experiment_values['duration'] = str(timedelta(seconds=experiment_values['duration']/(10**6)))

    experiment_start_unix =   int(time.mktime(time.strptime(str(experiment.start_time), '%Y-%m-%d %H:%M:%S')))*(10**6)
    experiment_sensors = experiment.sensors
    rock = Experiment.objects.filter(id=id).select_related('rock_id').values('rock_id', name=F('rock_id__name'))[0]

    query_time = '''
        SELECT t.time_micro
        FROM(SELECT(measurement.time_micro-{})::float/1000000 AS time_micro,  row_number() OVER(ORDER BY time_micro ASC) AS row
        	 FROM measurement
        	 WHERE  measurement.experiment_id ={} AND measurement.sensor_id={}) AS t
        WHERE t.row % {}=0;
    '''

    query_value = '''
        SELECT t.value
        FROM(SELECT  measurement.value AS value , row_number() OVER(ORDER BY time_micro ASC) AS row
        	 FROM measurement
        	 WHERE  measurement.experiment_id ={} AND measurement.sensor_id={}) AS t
        WHERE t.row % {}=0;
    '''

    fig = plt.figure()
    ax = plt.subplot(111)


    with connection.cursor() as cursor:
        cursor.execute(query_time.format(experiment_start_unix, id, sensors[0], downsample_val))
        time_arr = cursor.fetchall()

    for sens_id in sensors:
        sensor = Sensor.objects.get(id=sens_id)
        with connection.cursor() as cursor:
            cursor.execute(query_value.format(id, sens_id, downsample_val))
            data = cursor.fetchall()
        ax.plot(time_arr, data, label=sensor.name+" ({})".format(sensor.unit_of_measure))

    if os.path.isdir(graphs_dir)==False:
        os.mkdir(graphs_dir)

    plt.title('Drilling experiment data')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Measurement value")
    filename = str(uuid.uuid4())
    fig.set_size_inches(12, 7)
    ax.legend(loc='upper center', fontsize='small', ncol=6)
    fig.savefig(graphs_dir+'{}.png'.format(filename), dpi=80, bbox_inches='tight')
    ax.legend()


    return HttpResponse(json.dumps({'rock': rock, 'filename':filename, 'n_data_points':len(time_arr)*len(sensors), 'experiment':experiment_values}))



def generate_experiment(experiment_id):
    chunk_size=10000
    experiment = Experiment.objects.get(id=experiment_id)


    experiment_start_unix = int(experiment.start_time.timestamp())*(10**6)#int(time.mktime(time.strptime(experiment.start_time, '%Y-%m-%d %H:%M:%S+00:00')))*(10**6)
    print(experiment_start_unix)
    sensors = list(Sensor.objects.filter(id__in=experiment.sensors).values('abbreviation'))


    columns = "time_micro"
    for sensor in sensors:
        columns+= ","+sensor['abbreviation']
    yield columns+"\r\n"

    chunk = 0
    interval = 5*(10**6)
    while True:
        data = Measurement.objects.values('time_micro', 'value', 'sensor_id').filter(experiment_id=experiment_id, time_micro__gte=chunk*interval+experiment_start_unix, time_micro__lt=chunk*interval+interval+experiment_start_unix).order_by('time_micro','sensor_id')#[chunk*chunk_size:chunk*chunk_size+chunk_size]
        if len(data)==0:
            break
        row = ''
        i=0
        for measurement in data:
            if i==0:
                row +=str(round((measurement['time_micro']-experiment_start_unix)/(10**6),6) )+','+str(measurement['value'])
            else:
                row += ','+str(measurement['value'])
            i+=1
            if i==len(sensors):
                yield row+'\r\n'
                row=''
                i=0
        chunk +=1


def read_file(experiment_id):
    checksum = Experiment.objects.get(id=experiment_id).checksum
    dir_path = 'media/datasets/'+checksum+"/"
    dataset_path = dir_path+"dataset.csv"
    meta_file = dir_path+"metadata.json"

    with open(dataset_path, "r") as file:
        chunk = file.read(100000)
        while chunk:
            yield chunk
            chunk = file.read(100000)




@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def download_dataset(request, experiment_id):
    response = StreamingHttpResponse(read_file(experiment_id))
    exp_date = Experiment.objects.values('start_time').filter(id=experiment_id)[0]['start_time'].strftime( "%d-%B-%Y")
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=Experiment_'+exp_date+'.csv'

    return response
