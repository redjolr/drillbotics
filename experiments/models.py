from django.db import models
from rocks.models import Rock
from sensors.models import Sensor

class Experiment(models.Model):
    start_time = models.DateTimeField()
    description = models.TextField()
    rock_id = models.ForeignKey(Rock, db_column = 'rock_id', on_delete = models.PROTECT)


    class Meta:
        db_table = 'experiment'



class Measurement(models.Model):
    experiment_id = models.ForeignKey(Experiment, db_column = 'experiment_id', on_delete = models.CASCADE)
    sensor_id = models.ForeignKey(Sensor, db_column = 'sensor_id', on_delete = models.PROTECT)
    time_micro = models.BigIntegerField(Sensor)
    value = models.FloatField()          #Double precision in Postgresql
    depth = models.FloatField(null=True)

    class Meta:
        db_table = 'measurement'