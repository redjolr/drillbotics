from django.db import models
from django.contrib.auth.models import User, Group


#
User.add_to_class('occupation', models.CharField(max_length=100, null=True))
Group.add_to_class('added_time',  models.DateTimeField(auto_now_add=True, null=True))
Group.add_to_class('description',  models.CharField(max_length=200, null=True))
