from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    contact = models.BigIntegerField()
    tic_no = models.BigIntegerField()
    tic = models.CharField(max_length=50)

    class Meta:
        db_table = "school"
    
    def __str__(self):
        return self.name