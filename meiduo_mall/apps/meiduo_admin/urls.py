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
    # 统计今天注册人数
    url(r'^statistical/day_increment/$', statistical.TodayView.as_view()),
    # # 日活跃用户统计
    url(r'^statistical/day_active/$', statistical.ActiveView.as_view()),
    # 日下单用户量统计
    url(r'^statistical/day_orders/$', statistical.OrderView.as_view()),
    # 月增用户统计
    url(r'^statistical/month_increment/$', statistical.MonthView.as_view()),
    # 日分类商品访问量
    url(r'^statistical/goods_day_views/$', statistical.GoodsView.as_view()),

]
