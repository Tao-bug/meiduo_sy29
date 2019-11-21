import json
import re
from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection
from pymysql import DatabaseError

from apps.carts.utils import merge_cart_cookie_to_redis
from apps.oauth.models import OAuthQQUser, OAuthSinaUser
from apps.users.models import User
from utils.secret import SecretOauth
from utils.sinaweibopy3 import APIClient


# 绑定用户提交
class SinaAuthBindView(View):
    """绑定用户提交"""
    def post(self, request):
        # 接收参数
        json_dict = json.loads(request.body.decode())
        mobile = json_dict.get('mobile')
        password = json_dict.get('password')
        sms_code = json_dict.get('sms_code')
        uid = json_dict.get('uid')
        # uid 解密
        uid = SecretOauth().loads(uid).get('uid')

        # 校验
        if not uid:
            return http.JsonResponse({'status': 5003, 'errmsg': 'uid无效'})

        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')

        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        # 判断短信验证码是否一致
        sms_client = get_redis_connection('sms_code')
        sms_client_code = sms_client.get("sms_%s" % mobile)
        if sms_client_code is None:
            return http.JsonResponse({'status': 5001, 'errmsg': '无效短信验证码'})
        if sms_code != sms_client_code.decode():
            return http.JsonResponse({'status': 5002, 'errmsg': '输入短信验证码有误'})

        # 绑定用户
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在就创建用户
            user = User.objects.create(username=mobile, password=password, mobile=mobile)
        else:
            # 用户存在 --  检查用户密码
            if not user.check_password(password):
                return http.JsonResponse({'status': 5004, 'errmsg': '用户名或密码错误'})
        # 将用户绑定openid
        try:
            OAuthSinaUser.objects.create(user=user, uid=uid)
        except DatabaseError:
            return http.HttpResponseForbidden('绑定出错')
        # 绑定了就保持登陆状态
        login(request, user)
        response = http.JsonResponse({'status': 5000, 'errmsg': '绑定成功'})
        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response


# 用户扫码登录的回调处理  绑定页面显示
class SinaAuthCallBackView(View):
    """绑定页面显示"""
    def get(self, request):
        # http://www.meiduo.site:8000/sina_callback/?code=a2d0f44c5dc45f74951e3b2b2cc87678
        # 解析ｃｏｄｅ
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('无效的code!')
        # 创建工具对象
        client = APIClient(
            # app_key： app_key值
            app_key=settings.APP_KEY,
            # app_secret：app_secret 值
            app_secret=settings.APP_SECRET,
            # redirect_uri ： 回调地址
            redirect_uri=settings.REDIRECT_URL
        )
        # code --> access_token
        result = client.request_access_token(code)
        access_token = result.access_token
        uid = result.uid

        # 判断uid是否绑定过
        try:
            oauth_user = OAuthSinaUser.objects.get(uid=uid)
        except OAuthSinaUser.DoesNotExist:
            # 没绑定-->到绑定页面(带着加密的uid)
            uid = SecretOauth().dumps({'uid': uid})
            return render(request, 'sina_callback.html', context={'uid': uid})

        else:
            # 绑定了就保持登陆状态
            sina_user = oauth_user.user
            login(request, sina_user)

            # 响应结果
            # 重定向到主页
            response = redirect(reverse('contents:index'))

            # 登录时用户名写入到cookie，有效期15天
            response.set_cookie('username', sina_user.username, max_age=3600 * 24 * 15)

            return response


# 返回微博登陆地址
class SinaAuthURLView(View):
    """提供微博登陆网页
    https://api.weibo.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=YOUR_REGISTERED_REDIRECT_URI
    """
    def get(self, request):

        # 生成对象
        client = APIClient(
            # app_key： app_key值
            app_key=settings.APP_KEY,
            # app_secret：app_secret 值
            app_secret=settings.APP_SECRET,
            # redirect_uri ： 回调地址
            redirect_uri=settings.REDIRECT_URL
        )
        # 生成跳转的授权地址
        login_url = client.get_authorize_url()

        return http.JsonResponse({"code": 0, "errmsg": '微博登录页面网址', "login_url": login_url})


# 判断是否绑定
def is_bind_openid(openid, request):
    # 绑定过----首页
    try:
        qq_user = OAuthQQUser.objects.get(openid=openid)
    except OAuthQQUser.DoesNotExist:
        # 未绑定---绑定页面
        # 给前端的数据加密
        openid = SecretOauth().dumps({'openid': openid})
        return render(request, 'oauth_callback.html', {'openid': openid})
    else:
        user = qq_user.user
        # 绑定---首页
        # 保持登陆状态
        login(request, user)

        # 重定向首页
        response = redirect(reverse("contents:index"))

        # 设置cookie
        response.set_cookie('username', user.username, max_age=14*24*3600)

        return response


# 用户扫码登录的回调处理QQAuthUserView
class QQAuthCallBackView(View):
    # code--token--openid--是否绑定
    def get(self, request):
        # / oauth_callback?code = 31FFB8402D24214889BA444821D3CC3E & state = % 2Finfo % 2F
        # 1.解析code
        code = request.GET.get('code')

        if not code:
            return http.HttpResponseForbidden('无效的code!')

        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        try:
            # code --- token
            token = oauth.get_access_token(code)

            # token --- openid
            openid = oauth.get_open_id(token)
        except Exception as e:
            return http.HttpResponseForbidden('认证失败')

        # 是否绑定
        response = is_bind_openid(openid, request)

        # 调用合并购物车
        merge_cart_cookie_to_redis(request=request, response=response)

        return response

    # 提交绑定信息
    def post(self, request):
        # 解析参数
        mobile = request.POST.get('mobile')
        pwd = request.POST.get('password')
        sms_code = request.POST.get('sms_code')
        openid = request.POST.get('openid')

        # 校验
        # 判断参数是否齐全
        if not all([mobile, pwd, sms_code]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断短信验证码是否一致
        # redis_conn = get_redis_connection('verify_code')
        # sms_code_server = redis_conn.get('sms_%s' % mobile)
        # if sms_code_server is None:
        #     return render(request, 'oauth_callback.html', {'sms_code_errmsg': '无效的短信验证码'})
        # if sms_code != sms_code_server.decode():
        #     return render(request, 'oauth_callback.html', {'sms_code_errmsg': '输入短信验证码有误'})

        # 解密出openid 再判断openid是否有效
        locals_openid_dict = SecretOauth().loads(openid)
        openid = locals_openid_dict.get('openid')
        if not openid:
            return render(request, 'oauth_allback.hml', {'openid_errmsg': '无效的openid'})

        # 判断用户是否存在
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 不存在----创建新用户
            user = User.objects.create_user(username=mobile, password=pwd, mobile=mobile)
        else:
            # 存在---校验密码
            if not user.check_password(pwd):
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})

        # 绑定openid
        try:
            OAuthQQUser.objects.create(user=user, openid=openid)
        except Exception as e:
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': 'QQ绑定失败'})

        # 保持登陆状态--设置cookie首页用户名-- 首页
        login(request, user)

        # 重定向首页
        response = redirect(reverse("contents:index"))

        # 设置cookie
        response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        return response


# 返回qq登录地址
class QQAuthURLView(View):
    """提供QQ登录页面网址
    https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=xxx&redirect_uri=xxx&state=xxx
    """
    def get(self, request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next = request.GET.get('next')

        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        # 获取QQ登录扫码页面，扫码后得到Authorization Code
        login_url = oauth.get_qq_url()

        return http.JsonResponse({'code': 0, 'errmsg': 'QQ登录页面网址', 'login_url': login_url})
