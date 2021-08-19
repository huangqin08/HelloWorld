# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DbFhdb(models.Model):
    fhdb_id = models.CharField(db_column='FHDB_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    backup_time = models.CharField(db_column='BACKUP_TIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sqlpath = models.CharField(db_column='SQLPATH', max_length=300, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='TYPE')  # Field name made lowercase.
    dbsize = models.CharField(db_column='DBSIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bz = models.CharField(db_column='BZ', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'db_fhdb'


class DbTimingbackup(models.Model):
    timingbackup_id = models.CharField(db_column='TIMINGBACKUP_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    jobname = models.CharField(db_column='JOBNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    create_time = models.CharField(db_column='CREATE_TIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS')  # Field name made lowercase.
    fhtime = models.CharField(db_column='FHTIME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    timeexplain = models.CharField(db_column='TIMEEXPLAIN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bz = models.CharField(db_column='BZ', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'db_timingbackup'


class HrRecruitmentCatch(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=50, blank=True, null=True)
    person_sum = models.CharField(max_length=10, blank=True, null=True)
    hiring_time = models.CharField(max_length=50, blank=True, null=True)
    position_info = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_desc = models.TextField(blank=True, null=True)
    company_address = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    create_by = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    update_by = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_recruitment_catch'


class HrResumeAlarm(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    chk_phone = models.CharField(max_length=2, blank=True, null=True)
    chk_work = models.CharField(max_length=2, blank=True, null=True)
    memo = models.CharField(max_length=500, blank=True, null=True)
    send_time = models.CharField(max_length=19, blank=True, null=True)
    send_user_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_resume_alarm'


class HrResumeAuth(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    education_info = models.TextField(blank=True, null=True)
    company_info = models.TextField(blank=True, null=True)
    is_job = models.CharField(max_length=500, blank=True, null=True)
    language_level = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    apply_job = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=50, blank=True, null=True)
    real_score = models.IntegerField(blank=True, null=True)
    hands_on = models.CharField(max_length=100, blank=True, null=True)
    job_ranking = models.CharField(max_length=100, blank=True, null=True)
    star_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_resume_auth'


class HrResumeAuthDetail(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_auth_id = models.CharField(max_length=40, blank=True, null=True)
    check_type = models.CharField(max_length=100, blank=True, null=True)
    check_score = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_resume_auth_detail'


class HrResumeBase(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    live_address = models.CharField(max_length=200, blank=True, null=True)
    native_place = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    work_process = models.IntegerField(blank=True, null=True)
    e_mail = models.CharField(max_length=100, blank=True, null=True)
    learn_certificate = models.CharField(max_length=50, blank=True, null=True)
    expect_salary = models.IntegerField(blank=True, null=True)
    current_salary = models.CharField(max_length=50, blank=True, null=True)
    job_status = models.CharField(max_length=10, blank=True, null=True)
    job_intention = models.CharField(max_length=500, blank=True, null=True)
    marriage = models.CharField(max_length=20, blank=True, null=True)
    politics_status = models.CharField(max_length=20, blank=True, null=True)
    self_evaluation = models.TextField(blank=True, null=True)
    create_time = models.CharField(max_length=20, blank=True, null=True)
    create_by = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    update_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    opt_status = models.CharField(max_length=10, blank=True, null=True)
    preapproval_time = models.CharField(max_length=20, blank=True, null=True)
    opt_user_id = models.CharField(max_length=40, blank=True, null=True)
    up_user_id = models.CharField(max_length=40, blank=True, null=True)
    job_type = models.CharField(max_length=10, blank=True, null=True)
    file_url = models.CharField(max_length=500, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    school_nature = models.CharField(max_length=50, blank=True, null=True)
    school_level = models.CharField(max_length=10, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    opt_time = models.CharField(max_length=20, blank=True, null=True)
    opt_date = models.CharField(max_length=10, blank=True, null=True)
    valid_time = models.CharField(max_length=20, blank=True, null=True)
    show_url = models.CharField(max_length=500, blank=True, null=True)
    view_url = models.CharField(max_length=1000, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    file_content = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    last_modified_time = models.CharField(max_length=20, blank=True, null=True)
    pdf_url = models.CharField(max_length=200, blank=True, null=True)
    img_url = models.CharField(max_length=2000, blank=True, null=True)
    sel_type = models.CharField(max_length=10, blank=True, null=True)
    memo = models.CharField(max_length=2000, blank=True, null=True)
    source_flag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_resume_base'


class HrResumeEducation(models.Model):
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
        db_table = 'hr_resume_education'


class HrResumeWorkprocess(models.Model):
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
        db_table = 'hr_resume_workprocess'


class HrReumeProjectprocess(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    project_name = models.CharField(max_length=200, blank=True, null=True)
    project_start_date = models.CharField(max_length=50, blank=True, null=True)
    project_end_date = models.CharField(max_length=50, blank=True, null=True)
    develop_environment = models.CharField(max_length=100, blank=True, null=True)
    use_technology = models.CharField(max_length=100, blank=True, null=True)
    project_job = models.CharField(max_length=50, blank=True, null=True)
    project_desc = models.TextField(blank=True, null=True)
    project_content = models.TextField(blank=True, null=True)
    create_by = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_by = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_reume_projectprocess'


class HrTempBase(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    resume_id = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    live_address = models.CharField(max_length=200, blank=True, null=True)
    native_place = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    work_process = models.IntegerField(blank=True, null=True)
    e_mail = models.CharField(max_length=100, blank=True, null=True)
    learn_certificate = models.CharField(max_length=50, blank=True, null=True)
    expect_salary = models.IntegerField(blank=True, null=True)
    current_salary = models.CharField(max_length=50, blank=True, null=True)
    job_status = models.CharField(max_length=10, blank=True, null=True)
    job_intention = models.CharField(max_length=500, blank=True, null=True)
    marriage = models.CharField(max_length=20, blank=True, null=True)
    politics_status = models.CharField(max_length=20, blank=True, null=True)
    self_evaluation = models.TextField(blank=True, null=True)
    create_time = models.CharField(max_length=20, blank=True, null=True)
    create_by = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    update_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    opt_status = models.CharField(max_length=10, blank=True, null=True)
    opt_user_id = models.CharField(max_length=40, blank=True, null=True)
    up_user_id = models.CharField(max_length=40, blank=True, null=True)
    job_type = models.CharField(max_length=10, blank=True, null=True)
    file_url = models.CharField(max_length=500, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    school_nature = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    opt_time = models.CharField(max_length=20, blank=True, null=True)
    valid_time = models.CharField(max_length=20, blank=True, null=True)
    imp_flag = models.CharField(max_length=10, blank=True, null=True)
    show_url = models.CharField(max_length=500, blank=True, null=True)
    view_url = models.CharField(max_length=500, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    file_content = models.TextField(blank=True, null=True)
    last_modified_time = models.CharField(max_length=20, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    pdf_url = models.CharField(max_length=200, blank=True, null=True)
    source_flag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_temp_base'


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


class HrTempProjectprocess(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    project_name = models.CharField(max_length=200, blank=True, null=True)
    project_start_date = models.CharField(max_length=50, blank=True, null=True)
    project_end_date = models.CharField(max_length=50, blank=True, null=True)
    develop_environment = models.CharField(max_length=100, blank=True, null=True)
    use_technology = models.CharField(max_length=100, blank=True, null=True)
    project_job = models.CharField(max_length=50, blank=True, null=True)
    project_desc = models.TextField(blank=True, null=True)
    project_content = models.TextField(blank=True, null=True)
    create_by = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_by = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_temp_projectprocess'


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


class HrUserResumeRead(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    uid = models.CharField(max_length=40)
    resume_id = models.CharField(max_length=40)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_user_resume_read'


class HrUserResumeRelation(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    uid = models.CharField(max_length=40, blank=True, null=True)
    resume_id = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hr_user_resume_relation'


class ImFgroup(models.Model):
    fgroup_id = models.CharField(db_column='FGROUP_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'im_fgroup'


class ImFriends(models.Model):
    friends_id = models.CharField(db_column='FRIENDS_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fusername = models.CharField(db_column='FUSERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ctime = models.CharField(db_column='CTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    allow = models.CharField(db_column='ALLOW', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fgroup_id = models.CharField(db_column='FGROUP_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dtime = models.CharField(db_column='DTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    bz = models.CharField(db_column='BZ', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'im_friends'


class ImHismsg(models.Model):
    hismsg_id = models.CharField(db_column='HISMSG_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    toid = models.CharField(db_column='TOID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(db_column='PHOTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ctime = models.CharField(db_column='CTIME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  # Field name made lowercase.
    dread = models.CharField(db_column='DREAD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    owner = models.CharField(db_column='OWNER', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'im_hismsg'


class ImImstate(models.Model):
    imstate_id = models.CharField(db_column='IMSTATE_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    online = models.CharField(db_column='ONLINE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    autograph = models.CharField(db_column='AUTOGRAPH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sign = models.CharField(db_column='SIGN', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'im_imstate'


class ImIqgroup(models.Model):
    iqgroup_id = models.CharField(db_column='IQGROUP_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    qgroups = models.TextField(db_column='QGROUPS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'im_iqgroup'


class ImQgroup(models.Model):
    qgroup_id = models.CharField(db_column='QGROUP_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(db_column='PHOTO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ctime = models.CharField(db_column='CTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'im_qgroup'


class ImSysmsg(models.Model):
    sysmsg_id = models.CharField(db_column='SYSMSG_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fromusername = models.CharField(db_column='FROMUSERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ctime = models.CharField(db_column='CTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='CONTENT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    isdone = models.CharField(db_column='ISDONE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dtime = models.CharField(db_column='DTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    qgroup_id = models.CharField(db_column='QGROUP_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dread = models.CharField(db_column='DREAD', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'im_sysmsg'


class ResPicture(models.Model):
    picture_id = models.CharField(db_column='PICTURE_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    parent_id = models.CharField(db_column='PARENT_ID', max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100)  # Field name made lowercase.
    filepath = models.CharField(db_column='FILEPATH', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ctime = models.CharField(db_column='CTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    uname = models.CharField(db_column='UNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    master = models.CharField(db_column='MASTER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    filesize = models.CharField(db_column='FILESIZE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='REMARKS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'res_picture'


class SysBdSchool(models.Model):
    code = models.CharField(max_length=40, blank=True, null=True)
    school = models.CharField(max_length=500, blank=True, null=True)
    business_scale = models.CharField(max_length=20, blank=True, null=True)
    nature = models.CharField(max_length=255, blank=True, null=True)
    peculiarity = models.CharField(max_length=50, blank=True, null=True)
    level985 = models.CharField(max_length=20, blank=True, null=True)
    level211 = models.CharField(max_length=20, blank=True, null=True)
    school_level = models.CharField(max_length=10, blank=True, null=True)
    net_url = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_bd_school'


class SysCodeeditor(models.Model):
    codeeditor_id = models.CharField(db_column='CODEEDITOR_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ftlnmame = models.CharField(db_column='FTLNMAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ctime = models.CharField(db_column='CTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    codecontent = models.TextField(db_column='CODECONTENT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_codeeditor'


class SysCodes(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    key_name = models.CharField(max_length=50, blank=True, null=True)
    dtype = models.CharField(max_length=20, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.CharField(max_length=19, blank=True, null=True)
    update_psn = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_codes'


class SysCreatecode(models.Model):
    createcode_id = models.CharField(db_column='CREATECODE_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    packagename = models.CharField(db_column='PACKAGENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    objectname = models.CharField(db_column='OBJECTNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fieldlist = models.TextField(db_column='FIELDLIST', blank=True, null=True)  # Field name made lowercase.
    createtime = models.CharField(db_column='CREATETIME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fhtype = models.CharField(db_column='FHTYPE', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_createcode'


class SysDictionaries(models.Model):
    dictionaries_id = models.CharField(db_column='DICTIONARIES_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    name_en = models.CharField(db_column='NAME_EN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bianma = models.CharField(db_column='BIANMA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    order_by = models.IntegerField(db_column='ORDER_BY')  # Field name made lowercase.
    parent_id = models.CharField(db_column='PARENT_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bz = models.CharField(db_column='BZ', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tbsname = models.CharField(db_column='TBSNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tbfield = models.CharField(db_column='TBFIELD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    yndel = models.CharField(db_column='YNDEL', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_dictionaries'


class SysFhbutton(models.Model):
    fhbutton_id = models.CharField(db_column='FHBUTTON_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shiro_key = models.CharField(db_column='SHIRO_KEY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bz = models.CharField(db_column='BZ', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_fhbutton'


class SysFhlog(models.Model):
    fhlog_id = models.CharField(db_column='FHLOG_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    opt_ip = models.CharField(db_column='OPT_IP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cztime = models.CharField(db_column='CZTIME', max_length=32, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_fhlog'


class SysFhsms(models.Model):
    fhsms_id = models.CharField(db_column='FHSMS_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    content = models.CharField(db_column='CONTENT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    to_username = models.CharField(db_column='TO_USERNAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    from_username = models.CharField(db_column='FROM_USERNAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    send_time = models.CharField(db_column='SEND_TIME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sanme_id = models.CharField(db_column='SANME_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_fhsms'


class SysFileHistory(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    opt_source = models.CharField(max_length=20, blank=True, null=True)
    opt_status = models.CharField(max_length=5, blank=True, null=True)
    create_time = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    up_psn_id = models.CharField(max_length=50, blank=True, null=True)
    last_modified_time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_file_history'


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
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=50, blank=True, null=True)
    update_time = models.CharField(max_length=19, blank=True, null=True)
    update_psn = models.CharField(max_length=50, blank=True, null=True)
    user_level = models.CharField(max_length=20, blank=True, null=True)
    company_trade = models.CharField(max_length=3, blank=True, null=True)
    session = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_member'


class SysMemberIntegral(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    uid = models.CharField(max_length=40, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    create_psn = models.CharField(max_length=50, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_member_integral'


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


class SysMenu(models.Model):
    menu_id = models.IntegerField(db_column='MENU_ID', primary_key=True)  # Field name made lowercase.
    menu_name = models.CharField(db_column='MENU_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    menu_url = models.CharField(db_column='MENU_URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parent_id = models.CharField(db_column='PARENT_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    menu_order = models.CharField(db_column='MENU_ORDER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    menu_icon = models.CharField(db_column='MENU_ICON', max_length=60, blank=True, null=True)  # Field name made lowercase.
    menu_type = models.CharField(db_column='MENU_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    menu_state = models.IntegerField(db_column='MENU_STATE', blank=True, null=True)  # Field name made lowercase.
    shiro_key = models.CharField(db_column='SHIRO_KEY', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_menu'


class SysRole(models.Model):
    role_id = models.CharField(db_column='ROLE_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    role_name = models.CharField(db_column='ROLE_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rights = models.CharField(db_column='RIGHTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parent_id = models.CharField(db_column='PARENT_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    add_qx = models.CharField(db_column='ADD_QX', max_length=255, blank=True, null=True)  # Field name made lowercase.
    del_qx = models.CharField(db_column='DEL_QX', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edit_qx = models.CharField(db_column='EDIT_QX', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cha_qx = models.CharField(db_column='CHA_QX', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rnumber = models.CharField(db_column='RNUMBER', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_role'


class SysRoleFhbutton(models.Model):
    rb_id = models.CharField(db_column='RB_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    role = models.ForeignKey(SysRole, models.DO_NOTHING, db_column='ROLE_ID', blank=True, null=True)  # Field name made lowercase.
    button = models.ForeignKey(SysFhbutton, models.DO_NOTHING, db_column='BUTTON_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_role_fhbutton'


class SysTradenews(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    news_title = models.CharField(max_length=255, blank=True, null=True)
    news_subtitle = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    news_text = models.TextField(blank=True, null=True)
    news_img = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_tradenews'


class SysUeditor(models.Model):
    ueditor_id = models.CharField(db_column='UEDITOR_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='CONTENT', blank=True, null=True)  # Field name made lowercase.
    content2 = models.TextField(db_column='CONTENT2', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_ueditor'


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
    update_time = models.CharField(max_length=20, blank=True, null=True)
    update_psn = models.CharField(max_length=20, blank=True, null=True)
    job_set = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_user'


class SysUserphoto(models.Model):
    userphoto_id = models.CharField(db_column='USERPHOTO_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    photo0 = models.CharField(db_column='PHOTO0', max_length=255, blank=True, null=True)  # Field name made lowercase.
    photo1 = models.CharField(db_column='PHOTO1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    photo2 = models.CharField(db_column='PHOTO2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    photo3 = models.CharField(db_column='PHOTO3', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sys_userphoto'
