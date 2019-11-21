
from django.conf.urls import url

from . import views

urlpatterns = [
    # 结算订单页面显示
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='settlement'),

    # 提交订单接口 orders/commit/
    url(r'^orders/commit/$', views.OrderCommitView.as_view(), name='commit'),

    # 展示提交订单成功页面orders/success/
    url(r'^orders/success/$', views.OrderSuccessView.as_view(), name='success'),

    # 我的订单  orders/info/(?P<page_num>\d+)/
    url(r'^orders/info/(?P<page_num>\d+)/$', views.OrderInfoView.as_view(), name='order_info'),

    # 展示商品评价页面 orders/comment/
    url(r'^orders/comment/$', views.OrderCommentView.as_view(), name='comment'),

    # 详情页展示评价信息  comments/(?P<sku_id>\d+)/
    url(r'^comments/(?P<sku_id>\d+)/$', views.OrderCommentInfoView.as_view()),

]
