from django.db import models

class APIClient(models.Model):

    version = models.CharField(max_length=64,null=False, unique=True)
    date = models.DateTimeField(auto_now_add=True, null=False)
    file = models.FileField(upload_to='api_clients/')


    class Meta:
        db_table = 'api_client'
