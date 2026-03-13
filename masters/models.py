from django.db import models

# Create your models here.

# class Gender(models.Model):
#     name = models.CharField(max_length=10, unique=True)

#     def __str__(self):
#         return self.name    


class MasterBase(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name

class AgeCategory(MasterBase):
    class Meta:
        db_table = "m_age_cat"

class Gender(MasterBase):
    class Meta:
        db_table = "m_gender"

class Diet(MasterBase):
    class Meta:
        db_table = "m_diet"        

class Section(MasterBase):
    class Meta:
        db_table = "m_sec"   

class Standard(MasterBase):
    class Meta:
        db_table = "m_standard"  

class YogaSubCat(MasterBase):
    class Meta:
        db_table = "m_yoga_sub_cat"  