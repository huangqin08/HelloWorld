#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   views_resumeedit.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/21 14:33   gxrao      1.0         None
'''
import logging
import uuid

import simplejson
from django.http import JsonResponse, HttpResponse

from backstage_ment.models import HrTempWorkprocess, HrTempEducation
from backstage_ment.modelserializer import ReadResumeBaseSerializer, SaveDataHrResumeBase, SaveDataHrTempBase, \
    ResumeWorkproSerializer, TempWorkproSerializer, ResumeEduSerializer, TempEduSerializer
from resume.models import HrResumeBase, HrTempBase, HrResumeWorkprocess, HrResumeEducation

logger = logging.getLogger('log')


def resumeedit(request):
    if request.method == 'GET':
        resume_id = request.GET.get('resume_id')

        resume_obj = HrResumeBase.objects.filter(pk=resume_id).first()
        logger.info('从HrResumeBase中检查简历结果为：{}'.format(resume_obj))
        if not resume_obj:
            resume_obj = HrTempBase.objects.filter(pk=resume_id).first()
            logger.info('从HrTempBase中检查简历结果为：{}'.format(resume_obj))

        # 将获取到的数据通过序列化进行展现
        serializer_obj = ReadResumeBaseSerializer(resume_obj)

        list = {}
        for k, v in serializer_obj.data.items():
            list[k] = '' if v == None else v

        # 准备给前端返回的数据信息
        response_data = {
            'status': 200,
            'msg': '数据查询成功',
            'data': list
        }
        return JsonResponse(response_data)
    elif request.method == 'POST':
        body_obj = simplejson.loads(request.body)
        resume_id = body_obj.get('id')
        work_pro = body_obj.get('workpro').__len__()
        education = body_obj.get('education').__len__()

        logger.info('要开始修改数据了')
        # 创建一个字典，用于搜集数据的保存状态
        output_status = {
            'resume_obj': False,
            'work_pro': [],
            'education': [],
        }

        if not resume_id:
            logger.info('查询关键resume_id丢失，程序无法继续')
            return JsonResponse({'status': 202, 'msg': '查询关键resume_id丢失，程序无法继续'})

        resume_obj = HrResumeBase.objects.filter(pk=resume_id).first()
        logger.info('从HrResumeBase中检查简历结果为：{}'.format(resume_obj))

        if not resume_obj:
            resume_obj = HrTempBase.objects.filter(pk=resume_id).first()
            logger.info('从HrTempBase中检查简历结果为：{}'.format(resume_obj))
            save_obj = SaveDataHrTempBase(instance=resume_obj, data=body_obj, partial=False)
            # 检查是否有需要修改的work_pro数据
            if work_pro > 0:
                logger.info('work_pro有{}条数据需要存储'.format(work_pro))
                for i in body_obj.get('workpro'):
                    # 判断id参数，如果没有id表示新增的数据，如果有id表示需要修改的数据
                    if not i.get('id'):
                        # 没有id需要新增数据，在当前字典中新增一个id信息
                        i['id'] = str(uuid.uuid1().hex)
                        logger.info('没有找到id信息，开始创建一个id：{}，本次操作为新增操作'.format(i['id']))
                    wp = HrTempWorkprocess.objects.filter(id=i.get('id')).first()
                    workpro_save_obj = TempWorkproSerializer(instance=wp, data=i, partial=False)

                    if workpro_save_obj.is_valid():
                        logger.info('{}操作成功'.format(i['id']))
                        workpro_save_obj.save()
                        output_status['work_pro'].append({i['id']: True})
                    else:
                        logger.info('{}操作失败：{}'.format(i['id'], workpro_save_obj.error_messages))
                        output_status['work_pro'].append({i['id']: workpro_save_obj.error_messages})
            # 检查是否有需要修改的education数据
            if education > 0:
                logger.info('education有{}条数据需要存储'.format(education))
                for i in body_obj.get('education'):
                    # 判断id参数，如果没有id表示新增的数据，如果有id表示需要修改的数据
                    if not i.get('id'):
                        # 没有id需要新增数据，在当前字典中新增一个id信息
                        i['id'] = str(uuid.uuid1().hex)
                        logger.info('没有找到id信息，开始创建一个id：{}，本次操作为新增操作'.format(i['id']))
                    ed = HrTempEducation.objects.filter(id=i.get('id')).first()
                    education_save_obj = TempEduSerializer(instance=ed, data=i, partial=False)

                    if education_save_obj.is_valid():
                        education_save_obj.save()
                        output_status['education'].append({i['id']: True})
                    else:
                        logger.info('{}操作失败：{}'.format(i['id'], education_save_obj.error_messages))
                        output_status['education'].append({i['id']: education_save_obj.error_messages})
        else:
            save_obj = SaveDataHrResumeBase(instance=resume_obj, data=body_obj, partial=False)
            # 检查是否有需要修改的work_pro数据
            if work_pro > 0:
                logger.info('work_pro有{}条数据需要存储'.format(work_pro))
                for i in body_obj.get('workpro'):
                    # 判断id参数，如果没有id表示新增的数据，如果有id表示需要修改的数据
                    if not i.get('id'):
                        # 没有id需要新增数据，在当前字典中新增一个id信息
                        i['id'] = str(uuid.uuid1().hex)
                    wp = HrResumeWorkprocess.objects.filter(id=i.get('id')).first()
                    workpro_save_obj = ResumeWorkproSerializer(instance=wp, data=i, partial=False)

                    if workpro_save_obj.is_valid():
                        workpro_save_obj.save()
                        output_status['work_pro'].append({i['id']: True})
                    else:
                        output_status['work_pro'].append({i['id']: workpro_save_obj.error_messages})
            # 检查是否有需要修改的education数据
            if education > 0:
                logger.info('education有{}条数据需要存储'.format(education))
                for i in body_obj.get('education'):
                    # 判断id参数，如果没有id表示新增的数据，如果有id表示需要修改的数据
                    if not i.get('id'):
                        # 没有id需要新增数据，在当前字典中新增一个id信息
                        i['id'] = str(uuid.uuid1().hex)
                    ed = HrResumeEducation.objects.filter(id=i.get('id')).first()
                    education_save_obj = ResumeEduSerializer(instance=ed, data=i, partial=False)

                    if education_save_obj.is_valid():
                        education_save_obj.save()
                        output_status['education'].append({i['id']: True})
                    else:
                        output_status['education'].append({i['id']: education_save_obj.error_messages})

        if save_obj.is_valid():
            save_obj.save()
            output_status['resume_obj'] = True
        else:
            output_status['resume_obj'] = save_obj.error_messages

        response_data = {
            'status': 200,
            'msg': '数据保存结果如下',
            'data': output_status
        }
        return JsonResponse(response_data)
