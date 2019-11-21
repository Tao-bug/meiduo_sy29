
from django.conf.urls import url

from . import views

urlpatterns = [
    # 1.获取 qq网址
    url(r'^qq/login/$', views.QQAuthURLView.as_view(), name='qqlogin'),
    # 2.ｑｑ回调网址 oauth_callback
    url(r'^oauth_callback/$', views.QQAuthCallBackView.as_view()),
    # 3.获取微博网址　sina/login/
    url(r'^sina/login/$', views.SinaAuthURLView.as_view(), name='sinalogin'),
    # 4.微博回调网址,绑定页面显示 sina_callback/
    url(r'^sina_callback/$', views.SinaAuthCallBackView.as_view()),
    # 5.绑定用户提交
    url(r'^oauth/sina/user/$', views.SinaAuthBindView.as_view()),

]
