from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from experiments.models import Experiment,Measurement
from sensors.models import Sensor
from django.contrib.auth.models import User
from accounts.accounts_utils import user_changed_password


@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def home(request):
    experiments_set = Experiment.objects.all().values()
    sensors = Sensor.objects.all()
    data_count_set =Measurement.objects.all().values('experiment_id').filter(sensor_id=1).annotate(total=Count('experiment_id'))    #Gets the count of data points for every experiment
    data_count = {experiment['experiment_id']:experiment['total'] for experiment in data_count_set}
    experiments = []
    for exp in experiments_set:
        exp['data_count'] = data_count[exp['id']]
        experiments.append(exp)

    return render(request, 'dashboard/home.html', {'experiments': experiments, 'sensors':sensors, 'data_count':data_count})
