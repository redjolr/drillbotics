from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table='material'




class Rock(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    picture = models.ImageField(upload_to="media/",  null=True)
    added_time = models.DateTimeField(auto_now_add=True, null=True)

    materials = models.ManyToManyField(Material, through='RockComposition')

    def __str__(self):
        return self.name
    class Meta:
        db_table='rock'

    # def description_short(self):
    #     return self.description[:300]

class RockComposition(models.Model):
    rock = models.ForeignKey(Rock, db_column='rock_id', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, db_column='material_id', on_delete=models.PROTECT)

    class Meta:
        db_table='rock_composition'














# class RockComposition(models.Model):
#     rock_id = models.ForeignKey(Rock, on_delete = models.CASCADE)
#     material_id = models.ForeignKey(Material, on_delete = models.PROTECT)
#
#     class Meta:
#         db_table='rock_composition'

#    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
