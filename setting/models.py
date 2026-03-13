from django.db import models

# Create your models here.

class School(models.Model):
    yob_min = models.PositiveSmallIntegerField()
    yob_max = models.PositiveSmallIntegerField()
    yoc = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "settings"
    
    def __str__(self):
        return self.name