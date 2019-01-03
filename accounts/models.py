from django.db import models
from django.contrib.auth.models import User, Group


User.add_to_class('occupation', models.CharField(max_length=100, null=True))
Group.add_to_class('added_time',  models.DateTimeField(auto_now_add=True, null=True))
Group.add_to_class('description',  models.CharField(max_length=200, null=True))


class Occupation(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        db_table='occupation'

class Specialization(models.Model):
    name = models.CharField

    def __str__(self):
        return self.name
    class Meta:
        db_table='specialization'

class SpecificOccupation(models.Model):
    occupation_id = models.ForeignKey(Occupation, db_column = 'occupation_id', on_delete = models.PROTECT)
    specialization_id = models.ForeignKey(Specialization, db_column = 'specialization_id', on_delete = models.PROTECT)
    def __str__(self):
        return self.name
    class Meta:
        db_table='specific_occupation'
