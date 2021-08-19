import logging
import random, string, json
import uuid
from datetime import datetime, timedelta
from io import BytesIO

import xlrd
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# Create your views here.

# 高级搜索条件获取
from django.shortcuts import render, redirect

from ThinkJob.settings import accessKeyId, accessSecret, SignName, TemplateCode, IMG_CODE_TIME
from commer.CacheCodeObj import CacheCode
from commer.CreateImgCode import create_validate_code
from commer.SysTradeNews import systradenews
from commer.ThisWeek import thisweek
from resume.models import HrResumeBase, HrResumeAuth, HrUserResumeRelation, HrUserResumeRead, HrTempBase
from system.modelserializer import SysTradenewsSerializer, SysTradenewsDetailSerializer
from userhr.models import SysMember

logger = logging.getLogger('log')


# 大屏数据统计
def data_statistics(request):
    if request.GET.get('time'):
        time = request.GET.get('time')
        today = request.GET.get('time')
    else:
        time = datetime.now().strftime('%Y-%m-%d')
        today = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # 后台开发
    backend_developers = HrResumeBase.objects.filter(Q(job_type='01') | Q(job_type='08') | Q(job_type='09')).count()
    # 前台开发
    frontend_developers = HrResumeBase.objects.filter(job_type='02').count()
    # 移动端开发
    mobile_developers = HrResumeBase.objects.filter(Q(job_type='03') | Q(job_type='04')).count()
    # 其他类型
    other_developers = HrResumeBase.objects.filter(Q(job_type='05') | Q(job_type='06') | Q(job_type='07')).count()
    # 总简历数
    resume_sum = backend_developers + frontend_developers + mobile_developers + other_developers

    # 前置审批总数
    opt_status_sum = HrResumeBase.objects.filter(preapproval_time=today).filter(
        Q(opt_status='1') | Q(opt_status='9')).count()

    # 前置审批通过数
    opt_success = HrResumeBase.objects.filter(preapproval_time=today).filter(opt_status='9').count()
    try:
        # 前置审批通过率
        # opt_passing_rate = '{:.0%}'.format(opt_success / opt_status_sum)
        opt_passing_rate = int(round(opt_success / opt_status_sum, 2) * 100)
    except:
        opt_passing_rate = 0
    # base表简历总数
    toaudit_resume = HrResumeBase.objects.filter(opt_date=today).filter(
        Q(opt_status='1') | Q(opt_status='9')).count()
    # 已审批简历总数
    audited_resume = HrResumeBase.objects.filter(status='1').filter(opt_date=today).count()
    try:
        # 已审批简历通过率
        # audited_passing_resume = '{:.0%}'.format(audited_resume / toaudit_resume)
        audited_passing_resume = int(round(audited_resume / toaudit_resume, 2) * 100)
    except:
        audited_passing_resume = 0

    # 昨日入库java简历数
    today_java_resume = HrResumeBase.objects.filter(job_type='01').filter(create_time__contains=today).count()
    # 昨日入库web前端H5简历数
    today_web_resume = HrResumeBase.objects.filter(job_type='02').filter(create_time__contains=today).count()
    # 昨日入库android简历数
    today_android_resume = HrResumeBase.objects.filter(job_type='03').filter(
        create_time__contains=today).count()
    # 昨日入库ios简历数
    today_ios_resume = HrResumeBase.objects.filter(job_type='04').filter(create_time__contains=today).count()
    # 昨日入库UI简历数
    today_ui_resume = HrResumeBase.objects.filter(job_type='05').filter(create_time__contains=today).count()
    # 昨日入库测试简历数
    today_test_resume = HrResumeBase.objects.filter(job_type='06').filter(create_time__contains=today).count()
    # 昨日入库linux运维简历数
    today_linux_resume = HrResumeBase.objects.filter(job_type='07').filter(create_time__contains=today).count()
    # 昨日入库php运维简历数
    today_php_resume = HrResumeBase.objects.filter(job_type='08').filter(create_time__contains=today).count()
    # 昨日入库python运维简历数
    today_python_resume = HrResumeBase.objects.filter(job_type='09').filter(create_time__contains=today).count()
    # 昨日入库产品经理运维简历数
    today_PM_resume = HrResumeBase.objects.filter(job_type='09').filter(create_time__contains=today).count()
    # 未知职位简历数
    today_NULL_resume = HrResumeBase.objects.filter(job_type='').filter(create_time__contains=today).count()

    # --------------------------本周注册企业列表-------------------------------
    q1 = Q()
    q1.connector = 'OR'
    obj = thisweek(time)
    for i in obj:
        q1.children.append(('create_time__contains', str(i.strftime('%Y-%m-%d'))))
    sysmember_obj = SysMember.objects.filter(q1).order_by('-create_time')
    company_name = []
    for i in sysmember_obj:
        company_name.append(i.company_name)

    # --------------------------企业查看简历次数排名-------------------------------
    readresume_rankings = HrUserResumeRead.objects.exclude(uid='NoLogin').values('uid').annotate(
        counts=Count('uid')).order_by('-counts')
    company_rankings = []
    for i in readresume_rankings:
        obj = SysMember.objects.get(id=i['uid'])
        company_rankings.append({'company_name': obj.company_name, 'check_resume_num': i['counts']})

    # --------------------------昨日上传简历数-------------------------------
    today_update_num = HrResumeBase.objects.filter(create_time__contains=today).count()
    today_tempbase_update_num = HrTempBase.objects.filter(create_time__contains=today).count()
    today_update_resume_num = today_update_num + today_tempbase_update_num

    # --------------------------获取企业的上传简历数-------------------------------
    update_company_rankings = {}
    updata_resume_num = HrResumeBase.objects.values('up_user_id').annotate(
        counts=Count('up_user_id')).order_by('-counts')
    tempbase_resume_num = HrTempBase.objects.values('up_user_id').annotate(
        counts=Count('up_user_id')).order_by('-counts')

    for i in updata_resume_num:
        try:
            obj = SysMember.objects.get(id=i['up_user_id'])
        except:
            logger.error('【error】>>>>>>>>>>>>>>>>>>>{}'.format(i['up_user_id']))
        if not update_company_rankings.get(obj.company_name):
            update_company_rankings[obj.company_name] = i['counts']
        else:
            update_company_rankings[obj.company_name] = update_company_rankings[obj.company_name] + i['counts']

    for i in tempbase_resume_num:
        try:
            obj = SysMember.objects.get(id=i['up_user_id'])
        except:
            logger.error('【error】>>>>>>>>>>>>>>>>>>>{}'.format(i['up_user_id']))
        if not update_company_rankings.get(obj.company_name):
            update_company_rankings[obj.company_name] = i['counts']
        else:
            update_company_rankings[obj.company_name] = update_company_rankings[obj.company_name] + i['counts']

    update_company_rankings = sorted(update_company_rankings.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    update_company_rankings_k = []
    update_company_rankings_v = []
    for k, v in enumerate(update_company_rankings):
        if k == 5:
            break
        update_company_rankings_k.append(v[0])
        update_company_rankings_v.append(v[1])

    # --------------------------获取企业下载的简历数-------------------------------
    download_company_rankings = []
    download_company_rankings_k = []
    download_company_rankings_v = []
    download_company_obj = HrUserResumeRelation.objects.filter(Q(type='down') | Q(type='view')).values('uid').annotate(
        counts=Count('uid')).order_by('-counts')
    for k, v in enumerate(download_company_obj):
        if k == 5:
            break
        obj = SysMember.objects.get(id=v['uid'])
        if obj.company_name.__len__() > 5:
            company_name_split = obj.company_name[:5] + '..'
        else:
            company_name_split = obj.company_name
        download_company_rankings.append([company_name_split, v['counts']])
        download_company_rankings_k.append(company_name_split)
        download_company_rankings_v.append(v['counts'])

        date = {
            'resume_sum': resume_sum,
            'backend_developers': backend_developers,
            'frontend_developers': frontend_developers,
            'mobile_developers': mobile_developers,
            'other_developers': other_developers,
            'opt_status_sum': opt_status_sum,
            'opt_success': opt_success,
            'opt_passing_rate': opt_passing_rate,
            'toaudit_resume': toaudit_resume,
            'audited_resume': audited_resume,
            'audited_passing_resume': audited_passing_resume,
            'today_java_resume': today_java_resume,
            'today_web_resume': today_web_resume,
            'today_android_resume': today_android_resume,
            'today_ios_resume': today_ios_resume,
            'today_ui_resume': today_ui_resume,
            'today_test_resume': today_test_resume,
            'today_linux_resume': today_linux_resume,
            'today_php_resume': today_php_resume,
            'today_python_resume': today_python_resume,
            'today_PM_resume': today_PM_resume,
            'today_NULL_resume': today_NULL_resume,
            'company_name': company_name,
            'company_rankings': company_rankings,
            'update_company_rankings': update_company_rankings,
            'update_company_rankings_k': update_company_rankings_k,
            'update_company_rankings_v': update_company_rankings_v,
            'today_update_resume_num': today_update_resume_num,
            'download_company_rankings': download_company_rankings,
            'download_company_rankings_k': download_company_rankings_k,
            'download_company_rankings_v': download_company_rankings_v
        }

    # 准备给前端返回的数据信息
    logger.info('获取到的数据：{}'.format(date))

    if request.method == 'GET':
        return render(request, 'research.html', locals())
    if request.method == 'POST':
        return JsonResponse(date)


# XLS的数据导入
def XLS_update(request):
    if request.method == 'GET':
        try:
            s = request.session['s']
            logger.info(s)
        except:
            s = {'msg': '请上传需要解析的数据'}
        return render(request, 'xsl_update.html', s)
    if request.method == 'POST':
        f = request.FILES.get('file_xls')
        excel_type = f.name.split('.')[-1]

        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            dic = {
                'resume_phone': None,
                'school': None,
                'education_info': None,
                'is_job': None,
                'company_info': None,
                'real_score': None,
                'hands_on': None,
                'expect_salary': None,
            }

            try:
                with transaction.atomic():  # 控制数据库事务交易
                    for i, v in enumerate(table.row_values(0)):
                        if '姓名' in v:
                            dic['name'] = i
                        if '联系方式' in v:
                            dic['resume_phone'] = i
                        if '职位' in v:
                            dic['job_type'] = i
                        if '学校' in v:
                            dic['school'] = i
                        if '在职状态' in v:
                            dic['is_job'] = i
                        if '上一家公司规模' in v:
                            dic['company_info'] = i
                        if '推荐评分' in v:
                            dic['real_score'] = i
                        if '平均换工作率' in v:
                            dic['hands_on'] = i
                        if '最低期望薪资' in v:
                            dic['expect_salary'] = i
                        if '工作年限（年）' in v:
                            dic['work_process'] = i

                    success = 0
                    error = []
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        phone = rowVlaues[dic['resume_phone']]
                        if phone is None or phone is '':
                            error.append('{}：这条数据缺少手机号'.format(rowVlaues[dic['name']]))
                            continue

                        phone = str(int(phone))

                        obj = HrResumeBase.objects.filter(phone=str(phone)).first()
                        if not obj:
                            error.append('{}：在数据库中没有找到对应的手机号{}'.format(rowVlaues[dic['name']], str(phone)))
                            continue

                        resume_id = obj.id
                        company_info = str(int(rowVlaues[dic['company_info']])) + '人以上企业经验'

                        is_job = rowVlaues[dic['is_job']]
                        if '离职' in is_job:
                            is_job = '离职'
                        elif '在职' in is_job:
                            is_job = '在职'

                        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        real_score = str(int(rowVlaues[dic['real_score']]))
                        hands_on = '平均换工作率{}年'.format(str(int(rowVlaues[dic['hands_on']])))
                        school = rowVlaues[dic['school']]

                        job_type = rowVlaues[dic['job_type']]
                        code = CacheCode().filter(dtype='job').filter(key_name__contains=job_type).values(
                            'code').first()
                        if not code:
                            code = None
                        else:
                            code = code['code']

                        work_process = str(int(rowVlaues[dic['work_process']]))
                        expect_salary = int(rowVlaues[dic['expect_salary']])

                        if expect_salary < 1000:
                            expect_salary = int(str(expect_salary) + '000')

                        return_obj = HrResumeAuth.objects.update_or_create(pk_id=resume_id, id=str(uuid.uuid1().hex),
                                                                           company_info=company_info,
                                                                           is_job=is_job,
                                                                           create_time=create_time,
                                                                           create_psn='XSL', real_score=real_score,
                                                                           hands_on=hands_on, star_level='4')
                        logger.info(
                            '简历id：{}，手机号：{}，学校：{}，上一家公司规模：{}，推荐评分：{}，平均换工作率：{}，数据库更新结果：{}'.format(
                                resume_id, phone,
                                school,
                                company_info, real_score,
                                hands_on, return_obj))
                        if return_obj[1]:
                            success = success + 1
                            obj.school = school
                            obj.work_process = work_process
                            obj.job_status = is_job
                            obj.expect_salary = expect_salary
                            obj.job_type = code
                            obj.save()

                    msg = '服务器解析完成'
                    sc = 'display:block;'
                    date = '表格数据：{}条，'.format(rows - 1)
                    date_success = success
                    date_error = rows - 1 - success
                    s = {'msg': msg, 'sc': sc, 'date': date, 'date_success': date_success, 'date_error': date_error,
                         'error': error}
                    request.session['s'] = s
            except:
                msg = '解析excel文件失败，请检查数据是否完整'
                sc = None
                date = None
                date_success = None
                date_error = None
                error = None
                logger.error('上传文件类型错误！')
                s = {'msg': msg, 'sc': sc, 'date': date, 'date_success': date_success, 'date_error': date_error,
                     'error': error}
                request.session['s'] = s
                logger.error('解析excel文件或者数据插入错误')
        else:
            msg = '解析excel文件失败，请检查数据是否完整'
            sc = None
            date = None
            date_success = None
            date_error = None
            logger.error('上传文件类型错误！')
            s = {'msg': msg, 'sc': sc, 'date': date, 'date_success': date_success, 'date_error': date_error}
            request.session['s'] = s
    return redirect('system:XLS_update')


# 行业数据新闻详情
def tradenews_detail(request):
    if request.method == 'GET':
        news_id = request.GET.get('news_id')
        news_obj = systradenews().filter(id=news_id).first()
        if not news_obj:
            return JsonResponse({'status': 303, 'msg': '没有找到对应的数据'})
        tradenews_obj = SysTradenewsDetailSerializer(news_obj)
        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': tradenews_obj.data
        }

        return JsonResponse(response_data)


# 行业数据新闻列表
def tradenews_list(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        page_size = request.GET.get('page_size', 10)
        tradenews_obj = systradenews().filter(status='1').order_by('-create_time')

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(tradenews_obj, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)
        tradenews_obj = SysTradenewsSerializer(page_article_list, many=True)
        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': {
                'page': page,
                'page_size': page_size,
                'page_amount': str(paginator.num_pages),
                'list_detail': tradenews_obj.data,
            }
        }

        return JsonResponse(response_data)


# 获取字典表信息
def search_criteria(request):
    if request.method == 'GET':
        codes = CacheCode().filter(status='1').all()
        logger.info('获取codes对应码')
        redis_codes = cache.get('codes')

        if not redis_codes:
            logger.info('从redis中读取codes信息失败，需要添加缓存信息')
        else:
            logger.info('从redis中读取codes信息成功，直接返回数据')
            # 准备给前端返回的数据信息
            return JsonResponse({'status': 200, 'msg': '已找到字典数据', 'data': redis_codes})

        # 设置全量数据列表
        all_list = []
        # 设置key种类列表
        list = []

        logger.info('开始从SQL中读取codes表，马上开始整理')
        # 设置字典信息的key值
        for k, i in enumerate(codes):
            if i.dtype not in list:
                list.append(i.dtype)
                all_list.append({'dtype': i.dtype, 'sublist': []})

        for k, i in enumerate(codes):
            for num, det in enumerate(all_list):
                if i.dtype == det['dtype']:
                    if not i.name == '未知':
                        det['sublist'].append({'name': i.name, 'code': i.code})

        logger.info('codes表整理完成')

        if not redis_codes:
            logger.info('确定redis中没有codes码，开始将SQL中整理好的codes码载入redis')
            cache.set('codes', all_list)

            logger.info('设定当前codes码永不过期')
            cache.persist('codes')

        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '已找到字典数据',
            'data': all_list
        }
        logger.info('字典信息已返回')
    return JsonResponse(response_data)


# 发送验证码接口
def message_code(reuqest):
    if reuqest.method == 'POST':
        phone = reuqest.POST.get('phone')

        logger.info('请求验证码的用户：{}'.format(phone))

        # 在发送验证码之前需要检查验证码有效期，如果在有效期内不直接发送验证码
        cache_phone_message = cache.get('phone_message:' + phone)

        if cache_phone_message:
            logger.info('redis服务器下该{}用户的验证码为：{}，还未过有效期'.format(phone, cache_phone_message))
            # 已经获取到缓存的手机号了
            # 准备给前端返回的数据信息
            return JsonResponse({'status': 405, 'msg': '验证码有效期内请勿重复申请'})

        # 生成6位随机验证码（string）
        # 先生成6位随机数列表：random.sample([x for x in string.ascii_letters + string.digits],6
        # 通过join将列表拼接字符串
        # kUEeBr
        # print("".join(random.sample([x for x in string.ascii_letters + string.digits], 6)))
        # 生成6位随机数，准备填充到短信验证码模版的code表中
        six_num = "".join(map(lambda x: random.choice(string.digits), range(6)))

        '''-------------------------------阿里的短信服务器调用代码-----------------------------------------'''
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', SignName)
        request.add_query_param('TemplateCode', TemplateCode)
        request.add_query_param('TemplateParam', {'code': six_num})

        response_message = client.do_action(request)
        logger.info('当前手机号：{}，验证码：{}，发送状态：{}'.format(phone, six_num, str(response_message, encoding='utf-8')))
        # python2:  print(response)

        response_message = json.loads(str(response_message, encoding='utf-8'))
        logger.info('短信服务器返回的消息：{}'.format(response_message))
        '''-------------------------------阿里的短信服务器调用代码-----------------------------------------'''

        if response_message['Code'] == 'OK':
            # 如果验证码发送成功，那需要把当前验证码加入到缓存中进行存储，设定短信10分钟内有效
            logger.info('验证码发送成功，有效期10分钟')
            cache.set('phone_message:' + phone, six_num, 60 * 10)
            # 准备给前端返回的数据信息
            return JsonResponse({'status': 200, 'msg': '验证码发送成功'})
        else:
            # 准备给前端返回的数据信息
            return JsonResponse({'status': 404, 'msg': str(response_message['Message'])})


# 获取图片验证码
def img_code(request):
    """
    获取验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    # 生成图片 img、数字代码 code，保存在内存中，而不是 Django 项目中
    img, code = create_validate_code()
    img.save(stream, 'PNG')

    # 生成一个CODE随机数用于验证码绑定
    CODE = str(uuid.uuid1().hex)

    # 将验证码加入到redis中进行缓存
    cache.set('IMG_CODE:' + CODE, code, IMG_CODE_TIME)

    # 将验证码与绑定的CODE写入session，用来给登陆接口验证使用
    # request.session['CODE'] = code
    logger.info('验证码：{}'.format(code))

    response = HttpResponse(stream.getvalue(), content_type="image/png")
    response.set_cookie('CODE', CODE)

    return response
