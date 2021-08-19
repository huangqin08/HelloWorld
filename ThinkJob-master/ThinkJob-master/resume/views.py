import logging

from django.core.paginator import Paginator
from django.http import JsonResponse

from commer.CheckResumeAuth import check_resumeauth
from commer.CollectResume import user_collect
from commer.ResumeEvaluating import resumeEvaluating
from commer.ResumeRead import resume_read
from commer.ResumeRecommend import recommend
from commer.SearchResume import search_resume_list_all, search_resume_condition_query, search_resume_job
from commer.TodayResumeDownloads import today_resume_downloads
from resume.models import HrResumeBase
from resume.modelserializer import HrResumeBaseSerializer, HrResumeAuthSerializer, BaseToWorkSerializer, \
    ResumeDetailSerializer

# Create your views here.
from system.modelserializer import HrResumeEvaluatingSerializer

logger = logging.getLogger('log')


# 简历评测接口
def resume_evaluating(request):
    if request.method == 'GET':
        news_obj = resumeEvaluating().first()
        tradenews_obj = HrResumeEvaluatingSerializer(news_obj)
        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': tradenews_obj.data
        }

        return JsonResponse(response_data)


# 简历推荐
def resume_recommend(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        page = request.POST.get('page')
        page_size = request.POST.get('page_size', 10)
        recommend_list = recommend()

        if not recommend_list:
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
            return JsonResponse(response_data)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(recommend_list, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)
        serializer_list = BaseToWorkSerializer(page_article_list, many=True, context={'uid': uid})

        # 创建一个空列表去装载数据
        list_detail = []

        for i in serializer_list.data:
            resume_use = {}
            for k, v in i.items():
                resume_use[k] = '' if v == None else v
            list_detail.append(resume_use)

        logger.info('搜索成功，数据量：{}'.format(list_detail.__len__()))
        logger.info('搜索成功，查询到是数据为：{}'.format(list_detail))

        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': {
                'page': page,
                'page_size': page_size,
                'page_amount': str(paginator.num_pages),
                'list_detail': list_detail,
            }
        }
        return JsonResponse(response_data)


# 简历详情数据展现
def resume_detail(request):
    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        uid = request.POST.get('uid')

        resumebase_obj = HrResumeBase.objects.filter(id=resume_id).first()
        if not resumebase_obj:
            return JsonResponse({'status': 803, 'msg': '这不是个有效的简历'})

        serializer_obj = ResumeDetailSerializer(resumebase_obj, context={'uid': uid})
        resume_date = {}

        if uid:
            num = today_resume_downloads(uid)
            resume_date['use_download_num'] = num
        else:
            resume_date['use_download_num'] = 0

        for k, v in serializer_obj.data.items():
            if k == 'live_address' and (v == None or v == ''):
                resume_date[k] = '未知'
            else:
                resume_date[k] = '' if v == None else v

        resume_read(request)
        logger.info('{}'.format(resume_date))
    return JsonResponse(resume_date)


# 新版职位搜索，在老版基础上输出了子表的关联数据
def new_job_search(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        search_job = request.POST.get('search_job')
        page = request.POST.get('page')
        page_size = request.POST.get('page_size', 10)

        # 如果未登录用户出现page_size值超出的情况，那么有可能有人直接请求接口获取数据，需要将数据进行强制
        if not uid and int(page_size) > 10:
            page_size = 10

        logger.info('用户的职位搜索参数为：{}'.format(search_job))
        if not uid and not search_job:
            logger.info('用户没有需要搜索的职位，按照全量搜索展现')
            return resume_list_all(request)

        resume_list = search_resume_job(uid, search_job)
        if not resume_list:
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
            return JsonResponse(response_data)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(resume_list, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)

        serializer_list = BaseToWorkSerializer(page_article_list, many=True, context={'uid': uid})

        # 创建一个空列表去装载数据
        list_detail = []

        for i in serializer_list.data:
            resume_use = {}
            for k, v in i.items():
                resume_use[k] = '' if v == None else v
            list_detail.append(resume_use)

        logger.info('搜索成功，数据量：{}'.format(list_detail.__len__()))
        logger.info('搜索成功，查询到是数据为：{}'.format(list_detail))

        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': {
                'page': page,
                'page_size': page_size,
                'page_amount': str(paginator.num_pages),
                'list_detail': list_detail,
            }
        }
        return JsonResponse(response_data)


# 职位搜索
def job_search(request):
    if request.method == 'POST':
        search_job = request.POST.get('search_job')
        page = request.POST.get('page')
        page_size = request.POST.get('page_size', 10)

        logger.info('用户的职位搜索参数为：{}'.format(search_job))
        if not search_job:
            logger.info('用户没有需要搜索的职位，按照全量搜索展现')
            return resume_list_all(request)

        resume_list = search_resume_job(search_job)
        if not resume_list:
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
            return JsonResponse(response_data)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(resume_list, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)

        serializer_list = HrResumeBaseSerializer(page_article_list, many=True)

        # 创建一个空列表去装载数据
        list_detail = []

        for i in serializer_list.data:
            resume_use = {}
            for k, v in i.items():
                resume_use[k] = '' if v == None else v
            list_detail.append(resume_use)

        logger.info('搜索成功，数据量：{}'.format(list_detail.__len__()))
        logger.info('搜索成功，查询到是数据为：{}'.format(list_detail))

        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': {
                'page': page,
                'page_size': page_size,
                'page_amount': str(paginator.num_pages),
                'list_detail': list_detail,
            }
        }
        return JsonResponse(response_data)


# 新版带参数的高级搜索条件，在老版基础上输出了子表的关联数据
def new_resume_search(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        page = request.POST.get('page')  # 请求的页码
        page_size = request.POST.get('page_size', 10)  # 每页显示的数量
        job = request.POST.get('job')  # 职位
        education = request.POST.get('education')  # 学历
        work_process = request.POST.get('work_process')  # 工作经验
        expectsalary = request.POST.get('expectsalary')  # 期望薪资
        isjob = request.POST.get('isjob')  # 是否在职
        education_way = request.POST.get('education_way')  # 学校性质
        school_type = request.POST.get('school_type')  # 学校等级
        payrange_start = request.POST.get('payrange_start')  # 薪资范围搜索，起始范围
        payrange_end = request.POST.get('payrange_end')  # 薪资范围搜索，结束范围

        # 如果未登录用户出现page_size值超出的情况，那么有可能有人直接请求接口获取数据，需要将数据进行强制
        if not uid and int(page_size) > 10:
            page_size = 10

        if not uid and int(page) > 1:
            return JsonResponse({'status': 201, 'msg': '用户未登录', 'data': {}})

        if not uid and not payrange_start and not payrange_end and not \
                job and not education and not work_process \
                and not expectsalary and not isjob and not \
                education_way and not school_type:
            logger.info('用户没有带任何的搜索条件')
            return new_resume_list_all(request)

        resume_list = search_resume_condition_query(uid=uid, job=job, education=education, work_process=work_process,
                                                    expectsalary=expectsalary, isjob=isjob, education_way=education_way,
                                                    school_type=school_type, payrange_start=payrange_start,
                                                    payrange_end=payrange_end)

        if not resume_list:
            logger.info('没有查询到数据，放弃缓存')
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
            return JsonResponse(response_data)
        else:
            # 查到了数据
            logger.info('已经搜索到了用户的查询数据共{}条'.format(resume_list.__len__()))
            logger.info('正在对数据进行分页操作')
            # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
            paginator = Paginator(resume_list, page_size)
            if paginator.num_pages < int(page):
                return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

            # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
            page_article_list = paginator.page(page)

            serializer_list = BaseToWorkSerializer(page_article_list, many=True, context={'uid': uid})

            # 创建一个空列表去装载数据
            list_detail = []

            for i in serializer_list.data:
                resume_use = {}
                for k, v in i.items():
                    resume_use[k] = '' if v == None else v
                list_detail.append(resume_use)

            # 准备给前端返回的数据信息
            response_data = {
                'status': 200,
                'msg': '数据查询成功',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': str(paginator.num_pages),
                    'list_detail': list_detail,
                }
            }
            return JsonResponse(response_data)


# 带参数的高级搜索条件
def resume_search(request):
    if request.method == 'POST':
        page = request.POST.get('page')  # 请求的页码
        page_size = request.POST.get('page_size', 10)  # 每页显示的数量
        job = request.POST.get('job')  # 职位
        education = request.POST.get('education')  # 学历
        work_process = request.POST.get('work_process')  # 工作经验
        expectsalary = request.POST.get('expectsalary')  # 期望薪资

        logger.info('page----->{}'.format(page))
        logger.info('page_size----->{}'.format(page_size))

        logger.info('job----->{}'.format(job))
        logger.info('education----->{}'.format(education))
        logger.info('workprocess----->{}'.format(work_process))
        logger.info('expectsalary----->{}'.format(expectsalary))

        if not job and not education and not work_process and not expectsalary:
            logger.info('用户没有带任何的搜索条件')
            return resume_list_all(request)

        resume_list = search_resume_condition_query(job=job, education=education, work_process=work_process,
                                                    expectsalary=expectsalary)

        if not resume_list:
            logger.info('没有查询到数据，放弃缓存')
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
            return JsonResponse(response_data)
        else:
            # 查到了数据
            logger.info('已经搜索到了用户的查询数据共{}条'.format(resume_list.__len__()))
            logger.info('正在对数据进行分页操作')
            # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
            paginator = Paginator(resume_list, page_size)
            if paginator.num_pages < int(page):
                return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

            # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
            page_article_list = paginator.page(page)

            serializer_list = HrResumeBaseSerializer(page_article_list, many=True)

            # 创建一个空列表去装载数据
            list_detail = []

            for i in serializer_list.data:
                resume_use = {}
                for k, v in i.items():
                    resume_use[k] = '' if v == None else v
                list_detail.append(resume_use)

            # 准备给前端返回的数据信息
            response_data = {
                'status': 200,
                'msg': '数据查询成功',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': str(paginator.num_pages),
                    'list_detail': list_detail,
                }
            }
            return JsonResponse(response_data)


# 新版全部简历列表，在老版基础上输出了子表的关联数据
def new_resume_list_all(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')  # 请求的页码
        page = request.POST.get('page')  # 请求的页码
        page_size = request.POST.get('page_size', 10)  # 每页显示的数量
        resume_list = search_resume_list_all()

        # 如果未登录用户出现page_size值超出的情况，那么有可能有人直接请求接口获取数据，需要将数据进行强制
        if not uid and int(page_size) > 10:
            page_size = 10

        # 判断是否查到了数据
        if resume_list:
            logger.info('用户的搜索目前有结果共{}条数据'.format(resume_list.__len__()))
            logger.info('开始对这些数据进行分页操作')

            # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
            paginator = Paginator(resume_list, page_size)
            if paginator.num_pages < int(page):
                return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

            # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
            page_article_list = paginator.page(page)
            serializer_list = BaseToWorkSerializer(page_article_list, many=True, context={'uid': uid})

            # 创建一个空列表去装载数据
            list_detail = []

            for i in serializer_list.data:
                resume_use = {}
                for k, v in i.items():
                    resume_use[k] = '' if v == None else v
                list_detail.append(resume_use)

            # 准备给前端返回的数据信息
            response_data = {
                'status': 200,
                'msg': '数据查询成功',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': str(paginator.num_pages),
                    'list_detail': list_detail,
                }
            }

        else:
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
        return JsonResponse(response_data)


# 全部简历列表
def resume_list_all(request):
    if request.method == 'POST':
        page = request.POST.get('page')  # 请求的页码
        page_size = request.POST.get('page_size', 10)  # 每页显示的数量

        logger.info('all_页面page----->{}'.format(page))
        logger.info('all_页面page_size----->{}'.format(page_size))

        resume_list = search_resume_list_all()

        # 判断是否查到了数据
        if resume_list:
            logger.info('用户的搜索目前有结果共{}条数据'.format(resume_list.__len__()))
            logger.info('开始对这些数据进行分页操作')

            # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
            paginator = Paginator(resume_list, page_size)
            if paginator.num_pages < int(page):
                return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

            # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
            page_article_list = paginator.page(page)

            serializer_list = HrResumeBaseSerializer(page_article_list, many=True)

            # 创建一个空列表去装载数据
            list_detail = []

            for i in serializer_list.data:
                resume_use = {}
                for k, v in i.items():
                    resume_use[k] = '' if v == None else v
                list_detail.append(resume_use)

            # 准备给前端返回的数据信息
            response_data = {
                'status': 200,
                'msg': '数据查询成功',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': str(paginator.num_pages),
                    'list_detail': list_detail,
                }
            }

        else:
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
        return JsonResponse(response_data)


# 获取核验简历结果pk
def check_resume_auth(request):
    if request.method == 'POST':
        resume_id = request.POST.get('resume_id')
        resume_auth = check_resumeauth(resume_id)

        if resume_auth:
            resume_auth_list = HrResumeAuthSerializer(resume_auth)

            # 下面的代码主要是为了去除值为None的结果
            list = {}
            for k, v in resume_auth_list.data.items():
                list[k] = '' if v == None else v

            # 准备给前端返回的数据信息
            response_data = {
                'status': 200,
                'msg': '已找到核验过的简历数据',
                'data': list
            }
            logger.info('已经找到该{}简历的核验信息：{}'.format(resume_id, response_data))
            return JsonResponse(response_data)
        else:
            logger.info('没有该{}简历的核验信息'.format(resume_id))
            return JsonResponse({'status': 601, 'msg': '没有找到相关简历核验数据', 'data': {}})


# 用户搜藏的简历列表
def collect_resumelist(request):
    if request.method == 'POST':
        page = request.POST.get('page')  # 请求的页码
        page_size = request.POST.get('page_size', 10)  # 每页显示的数量
        uid = request.POST.get('uid')  # 用户uuid
        search_criteria = request.POST.get('search_criteria')  # 职位搜索条件

        # 如果未登录用户出现page_size值超出的情况，那么有可能有人直接请求接口获取数据，需要将数据进行强制
        if not uid and int(page_size) > 10:
            page_size = 10

        logger.info('用户搜藏列表的搜索条件：page-->{},page_size-->{},uid-->{},search_criteria-->{}'.format(page, page_size, uid,
                                                                                                search_criteria))
        resume_list = user_collect(uid, search_criteria)

        if not resume_list:
            logger.info('按照con的搜索条件没有查询到符合要求的数据')
            # 准备给前端返回的数据信息
            response_data = {
                'status': 301,
                'msg': '没有查询到数据',
                'data': {
                    'page': page,
                    'page_size': page_size,
                    'page_amount': '',
                    'list_detail': [],
                }
            }
            return JsonResponse(response_data)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(resume_list, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)

        serializer_list = BaseToWorkSerializer(page_article_list, many=True, context={'uid': uid})

        # 创建一个空列表去装载数据
        list_detail = []

        for i in serializer_list.data:
            resume_use = {}
            for k, v in i.items():
                resume_use[k] = '' if v == None else v
            list_detail.append(resume_use)

        logger.info('搜索成功，数据量：{}'.format(list_detail.__len__()))
        logger.info('搜索成功，查询到是数据为：{}'.format(list_detail))

        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': {
                'page': page,
                'page_size': page_size,
                'page_amount': str(paginator.num_pages),
                'list_detail': list_detail,
            }
        }
        return JsonResponse(response_data)
