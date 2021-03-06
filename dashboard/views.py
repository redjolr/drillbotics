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
            exp['sensors'] = [{'id':sensor_id, 'name':Sensor.objects.get(id=sensor_id).name} for sensor_id in exp['sensors']]
            exp['uploaded_percentage'] = "{:.0%}".format((exp['uploaded_data_points']) / exp['nr_data_points'])
            experiments.append(exp)
    return render(request, 'dashboard/home.html', {'experiments': experiments})
