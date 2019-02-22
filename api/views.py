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

@csrf_exempt
def upload_chunk(request, checksum):
    root_dir = 'media/datasets/'
    dir_path = 'media/datasets/'+checksum+"/"
    dump_file = dir_path+"dataset.csv"
    meta_file = dir_path+"metadata.json"
    if request.method=="POST":
        if os.path.isdir(root_dir)==False:
            os.mkdir(root_dir)

        count_checksum = Experiment.objects.filter(checksum=checksum).count()
        if count_checksum>0:
            return HttpResponse('DATASET_ALREADY_IN_DB')

        if 'chunk' in request.POST:
            if os.path.exists(dir_path)==False:
                os.mkdir(dir_path)
                with open(dump_file, "w") as f:
                    f.write(request.POST['chunk'])
            else:
                with open(dump_file, "a") as f:
                    f.write(request.POST['chunk'])
            return HttpResponse('CHUNK_RECEIVED')

        if 'metadata' in request.POST:
            metadata = json.loads(request.POST["metadata"])
            with open(meta_file, "w") as f:
                json.dump(metadata, f)
            return HttpResponse('METADATA_RECEIVED')
        print("HAHAHA", checksum, len(request.POST['chunk']))



@csrf_exempt
def addexperiment(request, checksum):
    dir_path = 'media/datasets/'+checksum+"/"
    dump_file = dir_path+"dataset.csv"
    meta_file = dir_path+"metadata.json"
    if request.method=="POST":
        count_checksum = Experiment.objects.filter(checksum=checksum).count()
        if count_checksum>0:
            return HttpResponse('DATASET_ALREADY_IN_DB')
        print("Adding experiment yoo", checksum)
        with open(meta_file, "r") as f:
            experiment_meta = json.load(f)

        df = pd.read_csv(dump_file)
        experiment_start_unix =   int(time.mktime(time.strptime(experiment_meta['start_time'], '%Y-%m-%d %H:%M:%S')))*(10**6)

        df["time_micro"] = [int(x*(10**6))+experiment_start_unix for x in df["time"] ]
        sensors_abbrs = list(df.columns.values)
        sensors = { sensor['abbreviation']:sensor['id'] for sensor in list(Sensor.objects.filter(abbreviation__in=sensors_abbrs).values('abbreviation', 'id')) }

        rock = Rock.objects.get(id=experiment_meta['rock_id'])

        experiment = Experiment(start_time = experiment_meta['start_time'], description = experiment_meta['description'], rock_id=rock, checksum=checksum )
        experiment.save()



        sql = '''INSERT INTO measurement(time_micro, value, depth, experiment_id, sensor_id) VALUES(%s, %s, %s, %s, %s)'''
        chunk_size = 5000
        df_chunks = [pd.DataFrame(df[i:i+chunk_size]) for i in range(0, len(df), chunk_size) ]

        t1 = time.time()
        for chunk_ind, df_chunk in enumerate(df_chunks):
            print("Started chunk ", chunk_ind)
            bulk_measurements = []
            for sensor, sensor_id in sensors.items():
                for i in range(len(df_chunk)):
                    bulk_measurements.append( ( int(df_chunk['time_micro'][i+chunk_ind*chunk_size]), df_chunk[sensor][i+chunk_ind*chunk_size], 0, experiment.id, sensor_id) )
            with connection.cursor() as cursor:
                cursor.executemany(sql,bulk_measurements)
        t2 = time.time()
        print("Duration: ", t2-t1)


        # print("CHunks created")
        # for chunk_ind, df_chunk in enumerate(df_chunks):
        #     print("CHunk ind started", chunk_ind)
        #
        #     print("After bulk_sensors", chunk_ind)
        #     for sensor, sensor_id in sensors.items():
        #         bulk_sensors = []
        #         print("Started chunk ", chunk_ind, " Sensor: ", sensor)
        #         sensor_obj = Sensor.objects.get(id=sensor_id)
        #         print(sensor_obj)
        #         for i in range(len(df_chunk)):
        #             print("Started ", i)
        #             meas = Measurement(experiment_id=experiment,sensor_id = sensor_obj, time_micro = df_chunk['time_micro'][i],value = df_chunk[sensor][i])
        #             print(meas)
        #             bulk_sensors.append(meas)
        #             print(i, len(bulk_sensors))
        #         print("Finished Chunk ", chunk_ind, " Sensor: ", sensor)
        #     Measurement.objects.bulk_create(bulk_sensors[chunk_ind*chunk_size:chunk_ind*chunk_size+chunk_size])
        #     print("Chunk added", chunk_ind)
        return HttpResponse('EXPERIMENT_ADDED')


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
