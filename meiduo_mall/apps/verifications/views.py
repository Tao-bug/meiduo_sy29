from django import http
from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from django.views import View

from meiduo_mall.settings.dev import logger


class SMSCodeView(View):
    # sms_codes/(?P<mobile>1[3-9]\d{9})/
    def get(self, request, mobile):
        # 1.解析校验参数--mobile 不用校验
        uuid = request.GET.get('image_code_id')
        image_code = request.GET.get('image_code')

        # 2.校验图形验证码 如果正确 发送验证码, 不正确 直接返回
        # 2.1 根据uuid 去redis数据库查询 图片验证码
        from django_redis import get_redis_connection
        image_redis_client = get_redis_connection('verify_image_code')
        redis_img_code = image_redis_client.get('img_%s' % uuid)

        # 判断服务器返回的验证
        if redis_img_code is None:
            return http.HttpResponseForbidden('图形验证码失效了')

        # 如果有值 删除redis服务器上的图形验证码
        try:
            image_redis_client.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 2.2 和前端传过来的进行做对比
        # 千万注意: 在redis取出来的是 bytes 类型不能直接做对比 decode()
        if image_code.lower() != redis_img_code.decode().lower():
            return http.HttpResponseForbidden({'输入图形验证码有误'})

        # 3.生成短信验证码,redis-存储
        from random import randint
        sms_code = "%06d" % randint(0, 999999)
        sms_redis_client = get_redis_connection('sms_code')

        # 4.让第三方 容联云-给手机号-发送短信
        # from libs.yuntongxun.sms import CCP
        # #                        手机号           验证码  过期时间5分钟 ,类型默认1
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # print("当前验证码是:", sms_code)
        # 发送短信验证码
        # CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SEND_SMS_TEMPLATE_ID)

        # (异步发短信)
        # 获取redis里面的标识
        send_sms_flag = sms_redis_client.get('send_flag%s' % mobile)
        if send_sms_flag:
            return http.HttpResponseForbidden({'发送短信过于频繁'})
        # 如果 倒计时标识 不在

        # 管道
        pipeline = sms_redis_client.pipeline()
        pipeline.setex("sms_%s" % mobile, 300, sms_code)
        pipeline.setex('send_flag%s' % mobile, 60, 1)
        pipeline.execute()

        # Celery异步发送短信验证码
        from celery_tasks.sms.tasks import ccp_send_sms_code
        ccp_send_sms_code.delay(mobile, sms_code)
        print("当前验证码是:", sms_code)

        # 5.告诉前端短信发送完毕
        return JsonResponse({'code': '0', 'errmsg': '发送短信成功'})


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        # 生成图片验证码
        from libs.captcha.captcha import captcha
        text, image = captcha.generate_captcha()

        # 保存图片验证码
        from django_redis import get_redis_connection
        redis_client = get_redis_connection('verify_image_code')
        from apps.verifications import constants
        redis_client.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应图片验证码
        return http.HttpResponse(image, content_type='image/jpg')
