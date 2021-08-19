import datetime

from django.db import models


# Create your models here.
class SysMember(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    user_pwd = models.CharField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    link_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company_scale = models.CharField(max_length=10, blank=True, null=True)
    e_mail = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    attention_key = models.CharField(max_length=1000, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    last_ip = models.CharField(max_length=20, blank=True, null=True)
    last_time = models.CharField(max_length=19, blank=True, null=True)
    photo_url = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.CharField(max_length=19, blank=True, null=True)
    update_psn = models.CharField(max_length=50, blank=True, null=True)
    user_level = models.CharField(max_length=20, blank=True, null=True)
    company_trade = models.CharField(max_length=3, blank=True, null=True)
    session = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'sys_member'

class HrResumeAlarm(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    chk_phone = models.CharField(max_length=2,blank=True, null=True)
    chk_work = models.CharField(max_length=2,blank=True, null=True)
    memo = models.CharField(max_length=500, blank=True, null=True)
    send_time = models.CharField(max_length=19, blank=True, null=True)
    send_user_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hr_resume_alarm'

class SysMemberOpthistory(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    uid = models.CharField(max_length=40, blank=True, null=True)
    opt_type = models.CharField(max_length=11, blank=True, null=True)
    opt_cnt = models.IntegerField(blank=True, null=True)
    cur_integral = models.IntegerField(blank=True, null=True)
    total_integral = models.IntegerField(blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_member_opthistory'
