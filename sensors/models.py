from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)
    description = models.TextField()
    unit_of_measure = models.CharField(max_length=20)
    picture = models.ImageField(upload_to="media/",  null=True)
    type = models.CharField(
        max_length = 15,
        choices = ( ('Physical', 'PHYSICAL' ), ('Virtual', 'VIRTUAL') ),
        null=True
    )   #a virtual sensor is a sensor whose value is calculated from other real physical values
    added_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'sensor'

    def added_time_pretty(self):
        return self.added_time.strftime("%d %B %Y")

    def description_short(self):
        return self.description[:200]
