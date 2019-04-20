from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#判断手机号是否存在
# 请求方式： GET / users / phones / (?P < mobile > 1[345789]\d{9}) / count /
# 接受mobile 	str 	手机号

# 返回mobile 	str 	手机号
#     count 	int 	数量
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.yuntongxun.sms import CCP

"""
一.分析需求
二.步骤(大概的思路)
三.确定请求方式和路由
四.选取哪个视图(结合需求,使用排除法)
五.编码
"""
from django_redis import get_redis_connection
# 访问方式： GET /verifications/imagecodes/(?P<image_code_id>.+)/
# image_code_id 	uuid字符串 	图片验证码编号
from libs.captcha.captcha import captcha
class RegisterImageCodeAPIView(APIView):
    def get(self,request,image_code_id):
        text,image=captcha.generate_captcha()
        redis_conn=get_redis_connection('code')
        redis_conn.setex('image_%s'%image_code_id,600,text)
        return HttpResponse(image,content_type='image/jepg')

# 短信验证码
# 业务处理流程
#
#     检查图片验证码
#     检查是否在60s内有发送记录
#     生成短信验证码
#     保存短信验证码与发送记录
#     发送短信
#
# 后端接口设计：
#
# 访问方式： GET /verifications/smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx & image_code_id=xxxx
# mobile 	        str 	    手机号
# image_code_id 	uuid字符串 	图片验证码编号
# text 	            str 	    用户输入的图片验证码
from .serializers import RegisterSmsCodeSerializer
class RegisterSmsCodeAPIView(APIView):
    def get(self,request,mobile):
        params = request.query_params
        # image_code_id=params.get('image_code_id')
        # text=params.get('text')
        serializer=RegisterSmsCodeSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        import random
        sms_code = '%06d' % random.randint(0, 999999)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)

        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile,sms_code)


        redis_conn=get_redis_connection('code')
        redis_conn.setex('sms_%s'%mobile,200,sms_code)
        return Response({'msg': 'ok'})