import string


from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from celery import shared_task





from experiments.models import Experiment, Measurement
from sensors.models import Sensor
from rocks.models import Rock
import json, os, time
from django.db import connection
import pandas as pd
import numpy as np
from django.db import transaction
import time


@shared_task
def add_experiment_to_db(checksum):
    dir_path = 'media/datasets/'+checksum+"/"
    dump_file = dir_path+"dataset.csv"
    meta_file = dir_path+"metadata.json"


    print("Adding experiment yoo", checksum)
    with open(meta_file, "r") as f:
        experiment_meta = json.load(f)
    sensors_abbrs = list(pd.read_csv(dump_file, nrows=1).columns)
    sensors_abbrs.remove('time')
    sensors = { sensor['abbreviation']:sensor['id'] for sensor in list(Sensor.objects.filter(abbreviation__in=sensors_abbrs).values('abbreviation', 'id')) }
    print("YOOOO", sensors_abbrs)
    with open(dump_file, "r") as f:
        num_lines = sum(1 for line in f) - 1



    experiment_start_unix =   int(time.mktime(time.strptime(experiment_meta['start_time'], '%Y-%m-%d %H:%M:%S')))*(10**6)
    rock = Rock.objects.get(id=experiment_meta['rock_id'])
    experiment = Experiment(start_time = experiment_meta['start_time'], description = experiment_meta['description'], rock_id=rock, checksum=checksum, nr_data_points=num_lines*len(sensors_abbrs) )
    experiment.save()
    sql = '''INSERT INTO measurement(time_micro, value, depth, experiment_id, sensor_id) VALUES(%s, %s, %s, %s, %s)'''

    t1 = time.time()
    chunk_ind=0
    chunk_size = 10000

    for df_chunk in pd.read_csv(dump_file, chunksize=chunk_size):
        print("Started chunk ", chunk_ind)
        df_chunk["time_micro"] = [int(x*(10**6))+experiment_start_unix for x in df_chunk["time"] ]
        bulk_measurements = []
        for sensor, sensor_id in sensors.items():
            for i in range(len(df_chunk)):
                bulk_measurements.append( ( int(df_chunk['time_micro'][i+chunk_ind*chunk_size]), df_chunk[sensor][i+chunk_ind*chunk_size], 0, experiment.id, sensor_id) )

        with connection.cursor() as cursor:
            cursor.executemany(sql,bulk_measurements)
            cursor.execute("UPDATE experiment SET uploaded_data_points = uploaded_data_points+%s WHERE id=%s ", [len(bulk_measurements), experiment.id])
        chunk_ind+=1


    t2 = time.time()
    return "Duration: {}".format(t2-t1)
