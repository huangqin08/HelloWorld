# Create your models here.

# Create your models here.
from django.db import models


class HrTempWorkprocess(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    work_start_date = models.CharField(max_length=50, blank=True, null=True)
    work_end_date = models.CharField(max_length=50, blank=True, null=True)
    work_nature = models.CharField(max_length=100, blank=True, null=True)
    work_job = models.CharField(max_length=100, blank=True, null=True)
    work_content = models.TextField(blank=True, null=True)
    create_by = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_by = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_temp_workprocess'

class HrTempEducation(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    in_school_date = models.CharField(max_length=50, blank=True, null=True)
    out_school_date = models.CharField(max_length=50, blank=True, null=True)
    learn_certificate = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    create_by = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_by = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_temp_education'