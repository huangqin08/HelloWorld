from django.db import models

# Create your models here.
class SysTradenews(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    news_title = models.CharField(max_length=255, blank=True, null=True)
    news_subtitle = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    news_text = models.TextField(blank=True, null=True)
    news_img = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'sys_tradenews'

class SysCodes(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    dtype = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    key_name = models.CharField(max_length=50, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.CharField(max_length=19, blank=True, null=True)
    update_psn = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_codes'

class SysUser(models.Model):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    role_id = models.CharField(db_column='ROLE_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    last_login = models.CharField(db_column='LAST_LOGIN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=32, blank=True, null=True)  # Field name made lowercase.
    bz = models.CharField(db_column='BZ', max_length=255, blank=True, null=True)  # Field name made lowercase.
    skin = models.CharField(db_column='SKIN', max_length=500, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=32, blank=True, null=True)  # Field name made lowercase.
    number = models.CharField(db_column='NUMBER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=32, blank=True, null=True)  # Field name made lowercase.
    role_ids = models.CharField(db_column='ROLE_IDS', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.user_id

    class Meta:
        managed = False
        db_table = 'sys_user'