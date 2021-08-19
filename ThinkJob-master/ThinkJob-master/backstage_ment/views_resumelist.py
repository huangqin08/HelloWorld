import logging

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
from backstage_ment.modelserializer import HrResumeBaseSerializer
from commer.CacheCodeObj import CacheCode
from resume.models import HrResumeBase, HrTempBase
from system.models import SysCodes

logger = logging.getLogger('log')


# 获取简历列表
def resumelist(request):
    if request.method == 'POST':
        list_type = request.POST.get('list_type')
        if list_type == '01':
            return notarize_resumelist(request)
        elif list_type == '02':
            return unconfirmed_resumelist(request)
        elif list_type == '03':
            return invalid_resumelist(request)


# 已确认简历列表高级搜索
def notarize_resumelist(request):
    if request.method == 'POST':
        page = request.POST.get('page')
        page_size = request.POST.get('page_size', 10)
        job = request.POST.get('job')
        job_status = request.POST.get('job_status')
        work_process = request.POST.get('work_process')
        sort = request.POST.get('sort')

        # 按照用户的排序规则，0是升序 1是降序，对update_time进行排序
        order_by = '-update_time'
        if sort in '0':
            order_by = 'update_time'

        q1 = Q()
        if job:
            q1.children.append(('job_type', job))

        if job_status:
            name = CacheCode().filter(code=job_status, dtype='isjob').values_list('name').first()
            q1.children.append(('job_status', name[0]))

        if work_process:
            name = CacheCode().filter(code=work_process, dtype='workprocess').values_list('name').first()
            logger.info('打印当前workprocess的code码信息--------->{}'.format(name))
            if '应届生' in name:
                q1.children.append(('work_process', '0'))
            elif '1年以内' in name:
                q1.children.append(('work_process__gt', '0'))
                q1.children.append(('work_process__lte', '1'))
            elif '1-3年' in name:
                q1.children.append(('work_process__gte', '1'))
                q1.children.append(('work_process__lt', '3'))
            elif '3-5年' in name:
                q1.children.append(('work_process__gte', '3'))
                q1.children.append(('work_process__lt', '5'))
            elif '5年及以上' in name:
                q1.children.append(('work_process__gte', '5'))

        logger.info('q1查询条件为：{}'.format(q1))

        # 已确认列表展现
        resume_list = HrResumeBase.objects.filter(status=1).filter(q1).all().order_by(order_by)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(resume_list, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)

        serializer_list = HrResumeBaseSerializer(page_article_list, many=True)

        logger.info('已查询列表第{}页的内容：{}'.format(page, serializer_list.data))

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


# 未确认简历列表高级搜索
def unconfirmed_resumelist(request):
    if request.method == 'POST':
        page = request.POST.get('page')
        page_size = request.POST.get('page_size', 10)
        job = request.POST.get('job')
        job_status = request.POST.get('job_status')
        work_process = request.POST.get('work_process')
        sort = request.POST.get('sort')

        # 按照用户的排序规则，0是升序 1是降序，对update_time进行排序
        order_by = '-update_time'
        if sort in '0':
            order_by = 'update_time'

        q1 = Q()
        if job:
            q1.children.append(('job_type', job))

        if job_status:
            name = CacheCode().filter(code=job_status, dtype='isjob').values_list('name').first()
            q1.children.append(('job_status', name[0]))

        if work_process:
            name = CacheCode().filter(code=work_process, dtype='workprocess').values_list('name').first()
            logger.info('打印当前workprocess的code码信息--------->{}'.format(name))
            if '应届生' in name:
                q1.children.append(('work_process', '0'))
            elif '1年以内' in name:
                q1.children.append(('work_process__gt', '0'))
                q1.children.append(('work_process__lte', '1'))
            elif '1-3年' in name:
                q1.children.append(('work_process__gte', '1'))
                q1.children.append(('work_process__lt', '3'))
            elif '3-5年' in name:
                q1.children.append(('work_process__gte', '3'))
                q1.children.append(('work_process__lt', '5'))
            elif '5年及以上' in name:
                q1.children.append(('work_process__gte', '5'))

        logger.info('q1查询条件为：{}'.format(q1))

        # 已确认列表展现
        resume_list = HrResumeBase.objects.filter(status=None).filter(q1).all().order_by(order_by)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(resume_list, page_size)
        if paginator.num_pages < int(page):
            return JsonResponse({'status': 300, 'msg': '分页超出最大值'})

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)

        serializer_list = HrResumeBaseSerializer(page_article_list, many=True)

        logger.info('已查询列表第{}页的内容：{}'.format(page, serializer_list.data))

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


# 已失效的简历列表高级搜索
def invalid_resumelist(request):
    if request.method == 'POST':
        page = request.POST.get('page')
        page_size = request.POST.get('page_size', 10)
        job = request.POST.get('job')
        job_status = request.POST.get('job_status')
        work_process = request.POST.get('work_process')
        sort = request.POST.get('sort')

        # 按照用户的排序规则，0是升序 1是降序，对update_time进行排序
        order_by = '-update_time'
        reverse = False
        if sort in '0':
            reverse = True
            order_by = 'update_time'

        q1 = Q()
        if job:
            q1.children.append(('job_type', job))

        if job_status:
            name = CacheCode().filter(code=job_status, dtype='isjob').values_list('name').first()
            q1.children.append(('job_status', name[0]))

        if work_process:
            name = CacheCode().filter(code=work_process, dtype='workprocess').values_list('name').first()
            logger.info('打印当前workprocess的code码信息--------->{}'.format(name))
            if '应届生' in name:
                q1.children.append(('work_process', '0'))
            elif '1年以内' in name:
                q1.children.append(('work_process__gt', '0'))
                q1.children.append(('work_process__lte', '1'))
            elif '1-3年' in name:
                q1.children.append(('work_process__gte', '1'))
                q1.children.append(('work_process__lt', '3'))
            elif '3-5年' in name:
                q1.children.append(('work_process__gte', '3'))
                q1.children.append(('work_process__lt', '5'))
            elif '5年及以上' in name:
                q1.children.append(('work_process__gte', '5'))

        logger.info('q1查询条件为：{}'.format(q1))

        # 无效的base表展现
        base_resume_list = HrResumeBase.objects.filter(Q(status=0) | Q(status=3)).filter(q1).all().order_by(order_by)
        # 无效的temp表展现
        temp_resume_list = HrTempBase.objects.filter(resume_id=None).all().order_by(order_by)

        # 将查询到的2组数据通过list的特性进行合并
        all_things = list(base_resume_list) + list(temp_resume_list)
        # 然后将合并后的数据进行update_time参数的降序排列
        sorted_things = sorted(all_things, key=lambda x: x.update_time, reverse=reverse)

        # 实例化一个分页组件，第一个参数是需要被分页的列表，第二个参数是每一个的item个数，比如这边指定每页个数为page_size
        paginator = Paginator(sorted_things, page_size)

        # page方法，传入一个参数，表示第几页的列表，这边传入的page，是你在地址中写的参数，传入page后返回该页面的所有数据page_article_list
        page_article_list = paginator.page(page)

        serializer_list = HrResumeBaseSerializer(page_article_list, many=True)

        logger.info('已查询列表第{}页的内容：{}'.format(page, serializer_list.data))

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
