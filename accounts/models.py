from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

User = get_user_model()

class Occupation(models.Model):
    name = models.CharField(max_length=50)
    random_str = models.CharField(max_length=1, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table='occupation'

class Specialization(models.Model):
    name = models.CharField(max_length=50)
    random_str = models.CharField(max_length=1, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table='specialization'

User.add_to_class('birthday', models.DateField(auto_now=False, auto_now_add=False, null=True))
User.add_to_class('picture', models.ImageField(upload_to="media/",  null=True))
User.add_to_class('occupation', models.ForeignKey(Occupation, db_column = 'occupation_id', on_delete = models.SET_NULL, null=True))
User.add_to_class('specialization', models.ForeignKey(Specialization, db_column = 'specialization_id', on_delete = models.SET_NULL, null=True))
User.add_to_class('password_changed', models.CharField(max_length=1, default ='f', null=False))
Group.add_to_class('added_time',  models.DateTimeField(auto_now_add=True, null=True))
Group.add_to_class('description',  models.CharField(max_length=200, null=True))
