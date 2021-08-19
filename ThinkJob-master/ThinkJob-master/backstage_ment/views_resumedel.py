import logging

from django.http import JsonResponse

# Create your views here.
from backstage_ment.models import HrTempWorkprocess, HrTempEducation
from backstage_ment.modelserializer import ResumeWorkproSerializer, TempWorkproSerializer, ResumeEduSerializer, \
    TempEduSerializer
from resume.models import HrResumeWorkprocess, HrResumeEducation

logger = logging.getLogger('log')


# 获取简历列表
def resumedel(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        workpro = HrResumeWorkprocess.objects.filter(id=id).first()
        temp_workpro = HrTempWorkprocess.objects.filter(id=id).first()
        edu = HrResumeEducation.objects.filter(id=id).first()
        temp_edu = HrTempEducation.objects.filter(id=id).first()
        t = False

        if workpro:
            logger.info('workpro里删除了这个{}的数据{}'.format(id, ResumeWorkproSerializer(workpro).data))
            workpro.delete()
            t = True

        if temp_workpro:
            logger.info('temp_workpro里删除了这个{}的数据{}'.format(id, TempWorkproSerializer(temp_workpro).data))
            temp_workpro.delete()
            t = True

        if edu:
            logger.info('edu里删除了这个{}的数据{}'.format(id, ResumeEduSerializer(workpro).data))
            edu.delete()
            t = True

        if temp_edu:
            logger.info('temp_edu里删除了这个{}的数据{}'.format(id, TempEduSerializer(workpro).data))
            temp_edu.delete()
            t = True

        if t:
            response_data = {'status': 200, 'msg': '操作成功'}
        else:
            response_data = {'status': 803, 'msg': '没有要删除的数据'}

        return JsonResponse(response_data)
