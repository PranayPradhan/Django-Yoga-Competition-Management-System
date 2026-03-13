from django.db import models

# Create your models here.

class Participant(models.Model):
    age_cat = models.ForeignKey(
        "masters.AgeCategory", on_delete=models.PROTECT, db_column="age_cat_id"
    )
    gender = models.ForeignKey(
        "masters.Gender", on_delete=models.PROTECT, db_column="gender_id"
    )
    school = models.ForeignKey(
        "school.School", on_delete=models.PROTECT, db_column="school_id"
    )
    yoga_sub_cat = models.ForeignKey(
        "masters.YogaSubCat", on_delete=models.PROTECT, db_column="yoga_sub_cat_id"
    )
    standard = models.ForeignKey(
        "masters.Standard", on_delete=models.PROTECT, db_column="standard_id"
    )
    sec = models.ForeignKey(
        "masters.Section", on_delete=models.PROTECT, db_column="sec_id"
    )
    diet = models.ForeignKey(
        "masters.Diet", on_delete=models.PROTECT, db_column="diet_id"
    )

    name = models.CharField(max_length=50)
    bib_no = models.PositiveSmallIntegerField(unique=True)
    yob = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "participant"

    def __str__(self):
        return f"{self.name} ({self.bib_no})"
