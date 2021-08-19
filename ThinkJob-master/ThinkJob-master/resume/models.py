from django.db import models


# Create your models here.
class HrResumeEvaluating(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    news_title = models.CharField(max_length=255, blank=True, null=True)
    news_text = models.TextField(blank=True, null=True)
    create_user = models.CharField(max_length=40, blank=True, null=True)
    create_time = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hr_resume_evaluating'


class HrResumeAuth(models.Model):
    id = models.CharField(primary_key=True, max_length=40, blank=True)
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

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hr_resume_auth'


class HrResumeAuthDetail(models.Model):
    id = models.CharField(primary_key=True, max_length=40, blank=True)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    check_type = models.CharField(max_length=10, blank=True, null=True)
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

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hr_resume_base'


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
    work_process = models.CharField(max_length=50, blank=True, null=True)
    e_mail = models.CharField(max_length=100, blank=True, null=True)
    learn_certificate = models.CharField(max_length=50, blank=True, null=True)
    expect_salary = models.IntegerField(blank=True, null=True)
    current_salary = models.CharField(max_length=50, blank=True, null=True)
    job_status = models.CharField(max_length=10, blank=True, null=True)
    marriage = models.CharField(max_length=20, blank=True, null=True)
    politics_status = models.CharField(max_length=20, blank=True, null=True)
    self_evaluation = models.TextField(blank=True, null=True)
    create_time = models.CharField(max_length=20, blank=True, null=True)
    create_by = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.CharField(max_length=20, blank=True, null=True)
    update_by = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    opt_status = models.CharField(max_length=10, blank=True, null=True)
    opt_user_id = models.CharField(max_length=40, blank=True, null=True)
    up_user_id = models.CharField(max_length=40, blank=True, null=True)
    job_type = models.CharField(max_length=10, blank=True, null=True)
    file_url = models.CharField(max_length=500, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    opt_time = models.CharField(max_length=20, blank=True, null=True)
    imp_flag = models.CharField(max_length=10, blank=True, null=True)
    show_url = models.CharField(max_length=500, blank=True, null=True)
    view_url = models.CharField(max_length=500, blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    last_modified_time = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hr_temp_base'


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


class HrUserResumeRelation(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    uid = models.CharField(max_length=40, blank=True, null=True)
    resume_id = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    integral = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hr_user_resume_relation'


class HrResumeEducation(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pk_id = models.CharField(max_length=40, blank=True, null=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    in_school_date = models.CharField(max_length=50, blank=True, null=True)
    out_school_date = models.CharField(max_length=50, blank=True, null=True)
    learn_certificate = models.CharField(max_length=50, blank=True, null=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    create_by = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_by = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.pk_id

    class Meta:
        managed = False
        db_table = 'hr_resume_education'


class HrUserResumeRead(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    uid = models.CharField(max_length=40)
    resume_id = models.CharField(max_length=40)
    create_time = models.CharField(max_length=19, blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'hr_user_resume_read'
