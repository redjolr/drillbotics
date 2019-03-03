from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from experiments.models import Experiment,Measurement
from sensors.models import Sensor
from django.contrib.auth.models import User
from accounts.accounts_utils import user_changed_password
from django.db import connection

@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def home(request):
    experiments_set = Experiment.objects.all().values()
    experiments = []
    with connection.cursor() as cursor:
        for exp in experiments_set:
            #Because it is not possible to do a GROUP BY using the ORM
            cursor.execute('''
                           SELECT id, name FROM sensor INNER JOIN (
                           SELECT sensor_id FROM measurement
                           WHERE experiment_id=%s
                           GROUP BY sensor_id) as grouped_sensors ON sensor.id=grouped_sensors.sensor_id''', [exp['id']])
            exp['sensors'] = [{'id':sensor[0], 'name':sensor[1]} for sensor in cursor.fetchall()]
            exp['uploaded_percentage'] = "{:.0%}".format((exp['uploaded_data_points']) / exp['nr_data_points'])
            experiments.append(exp)

    return render(request, 'dashboard/home.html', {'experiments': experiments})
