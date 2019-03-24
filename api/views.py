from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import ExperimentSerializer
from experiments.models import Experiment, Measurement
from sensors.models import Sensor
from rocks.models import Rock
import json, os, time
from django.db import connection
import pandas as pd
import numpy as np
from django.db import transaction
from django.conf import settings
import time, base64
from .tasks import add_experiment_to_db
from .models import APIClient

@csrf_exempt
def upload_chunk(request, checksum):
    root_dir = 'media/datasets/'
    dir_path = 'media/datasets/'+checksum+"/"
    dump_file = dir_path+"dataset.csv"
    meta_file = dir_path+"metadata.json"
    if request.method=="POST":
        auth = request.META['HTTP_AUTHORIZATION'].split()
        username, password = base64.b64decode( auth[1]).decode("utf-8").split(':')
        user = authenticate(username=username, password=password)
        if user is None or user.is_active==False:
            return HttpResponse('AUTHENTICATION_FAILED')


        if 'metadata' in request.POST:
            experiment_meta = json.loads(request.POST["metadata"])
            with open(meta_file, "a") as f:
                json.dump(experiment_meta, f)
            return HttpResponse('METADATA_RECEIVED')


        if  Experiment.objects.filter(checksum=checksum).exists():
            return HttpResponse('DATASET_ALREADY_IN_DB')
        if os.path.isdir(root_dir)==False:
            os.mkdir(root_dir)
        if os.path.isdir(dir_path)==False:
            os.mkdir(dir_path)
        if 'chunk' in request.POST:

            with open(dump_file, "a") as f:
                f.write(request.POST['chunk'])
            return HttpResponse('CHUNK_RECEIVED')



@csrf_exempt
def addexperiment(request, checksum):
    dir_path = 'media/datasets/'+checksum+"/"
    dump_file = dir_path+"dataset.csv"
    meta_file = dir_path+"metadata.json"

    if request.method=="POST":
        auth = request.META['HTTP_AUTHORIZATION'].split()
        username, password = base64.b64decode( auth[1]).decode("utf-8").split(':')
        user = authenticate(username=username, password=password)
        if user is None or user.is_active==False:
            return HttpResponse('AUTHENTICATION_FAILED')

        if Experiment.objects.filter(checksum=checksum).exists():
            return HttpResponse('DATASET_ALREADY_IN_DB')

        with open(meta_file, "r") as f:
            experiment_meta = json.load(f)
        sensors_abbrs = list(pd.read_csv(dump_file, nrows=1).columns)
        sensors_abbrs.remove('time')
        sensors = { sensor['abbreviation']:sensor['id'] for sensor in list(Sensor.objects.filter(abbreviation__in=sensors_abbrs).values('abbreviation', 'id')) }
        with open(dump_file, "r") as f:
            num_lines = sum(1 for line in f) - 1

        experiment_start_unix =   int(time.mktime(time.strptime(experiment_meta['start_time'], '%Y-%m-%d %H:%M:%S')))*(10**6)
        rock = Rock.objects.get(id=experiment_meta['rock_id'])
        experiment = Experiment(start_time = experiment_meta['start_time'], description = experiment_meta['description'], rock_id=rock, checksum=checksum, nr_data_points=num_lines*len(sensors_abbrs) )
        experiment.sensors = [ id for id in sensors.values() ]
        experiment.save()
        add_experiment_to_db.delay(checksum)
        return HttpResponse('EXPERIMENT_BEING_ADDED_TO_THE_DB')



@csrf_exempt
def getsensors(request):
    if request.method=="GET":
        sensors = [ sensor['abbreviation'] for sensor in list(Sensor.objects.values('abbreviation')) ]
        return HttpResponse(json.dumps(sensors))

@csrf_exempt
def getrocks(request):
    if request.method=="GET":
        rocks = [ rock['name'] for rock in list(Rock.objects.values('name')) ]
        return HttpResponse(json.dumps(rocks))

@csrf_exempt
def get_initial_data(request):
    if request.method=="GET":
        auth = request.META['HTTP_AUTHORIZATION'].split()
        username, password = base64.b64decode( auth[1]).decode("utf-8").split(':')
        user = authenticate(username=username, password=password)
        if user is None or user.is_active==False:
            return HttpResponse('AUTHENTICATION_FAILED')

        sensors = [ sensor for sensor in list(Sensor.objects.values('abbreviation', 'id')) ]
        rocks = [ rock for rock in list(Rock.objects.values('name', 'id')) ]
        api_latest = APIClient.objects.all().order_by('-date')[0]
        return HttpResponse(json.dumps({'rocks':rocks, 'sensors':sensors, 'api_version':api_latest.version}))


def download_api_client(request):
    api_latest = APIClient.objects.all().order_by('-date')[0]
    file_path = os.path.join(settings.MEDIA_ROOT, str(api_latest.file))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inltine; filename='+os.path.basename(file_path)
            return response
    else:
        return HttpResponse("ERROR! File no longer exists in the server")
