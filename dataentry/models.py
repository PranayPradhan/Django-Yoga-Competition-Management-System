from django.db import models

# Create your models here.
class ScoreIndividual(models.Model):
    yoga_sub_cat = models.ForeignKey(
        "masters.YogaSubCat", on_delete=models.PROTECT, db_column="yoga_sub_cat_id"
    )
    age_cat = models.ForeignKey(
        "masters.AgeCategory", on_delete=models.PROTECT, db_column="age_cat_id"
    )
    gender = models.ForeignKey(
        "masters.Gender", on_delete=models.PROTECT, db_column="gender_id"
    )

    bib_no = models.PositiveSmallIntegerField()   

    value = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    coc_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    is_coc = models.BooleanField(default=False)

    class Meta:
        db_table = "score_individual"

    def __str__(self):
        return f"{self.bib_no}"
