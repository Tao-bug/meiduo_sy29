from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical
from .views import admin

urlpatterns = [
    # 基于只使用django 包时　　ｊｗｔ代码的实现
    # url(r'^authorizations/$', admin.LoginView.as_view()),
    # url(r'^statistical/total_count/', admin.TestView.as_view()),

    # 基于drf 时　可以借助drf-jwt　包实现
    url(r'^authorizations/$', obtain_jwt_token),
    # 统计总数
    url(r'^statistical/total_count/$', statistical.TotalView.as_view()),


]
