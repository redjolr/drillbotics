from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse, HttpResponse
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
import time
from .tasks import add_experiment_to_db


@csrf_exempt
def upload_chunk(request, checksum):
    root_dir = 'media/datasets/'
    dir_path = 'media/datasets/'+checksum+"/"
    dump_file = dir_path+"dataset.csv"
    meta_file = dir_path+"metadata.json"
    if request.method=="POST":
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

        if 'metadata' in request.POST:
            metadata = json.loads(request.POST["metadata"])
            with open(meta_file, "a") as f:
                json.dump(metadata, f)
            return HttpResponse('METADATA_RECEIVED')



@csrf_exempt
def addexperiment(request, checksum):
    if request.method=="POST":
        if Experiment.objects.filter(checksum=checksum).exists():
            return HttpResponse('DATASET_ALREADY_IN_DB')

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
def getrocksandsensors(request):
    if request.method=="GET":
        sensors = [ sensor for sensor in list(Sensor.objects.values('abbreviation', 'id')) ]
        rocks = [ rock for rock in list(Rock.objects.values('name', 'id')) ]
        return HttpResponse(json.dumps({'rocks':rocks, 'sensors':sensors}))
