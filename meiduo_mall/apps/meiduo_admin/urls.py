from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import statistical, user, spec, spu, sku, category, images, orders, permission, groups, brands
from rest_framework.routers import SimpleRouter
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

    # 用户的查询获取
    url(r'^users/$', user.UserView.as_view()),
    # spu
    url(r'^goods/simple/$', spu.SpuSimpleView.as_view()),
    # sku-第三级分类
    url(r'^skus/categories/$', category.Category3View.as_view()),
    # 根据spu查询spec的路由goods/1/specs/
    url(r'^goods/(?P<spu_id>\d+)/specs/$', spec.SpecBySpuView.as_view()),
    # 查询所有的sku，返回简单数据，用于添加商品图片时的选择
    url(r'^skus/simple/$', sku.SkuSimpleView.as_view()),
    # 为订单修改状态的方法配置路由规则
    # url('^orders/(?P<pk>\d+)/status/$',orders.OrderViewSet.as_view({'put':'status'})),
    # 权限
    url(r'^permission/perms/$', permission.PermissionView.as_view()),
    # 权限选择数据(简单查询)
    url(r'^permission/simple/$', permission.PermissionSimpleView.as_view()),
    # 简单品牌信息
    url(r'^goods/brands/simple/$', spu.BrandsSimpleView.as_view()),
    # 获取一级分类信息
    url(r'^goods/channel/categories/$', category.Category1View.as_view()),
    # 获取二、三级分类信息
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', category.CategoryView.as_view()),
    # spu上传图片
    url(r'^goods/images/$', images.SpuImageView.as_view()),
    # 下拉菜单获取品牌信息
    url(r'^goods/specs/simple/$', spec.SpecSimpleView.as_view()),


]

router = SimpleRouter()
# 为规格spec注册路由
router.register('goods/specs', spec.SpecViewSet, base_name='specs')

# 为sku图片注册
# 注意：必须写在skus路由规则的上面
router.register('skus/images', images.ImageViewSet, base_name='images')

# 为sku注册
router.register('skus', sku.SkuViewSet, base_name='skus')

# 订单
router.register('orders', orders.OrderViewSet, base_name='orders')

# 组
router.register('permission/groups', groups.GroupViewSet, base_name='groups')

# 获取管理员用户列表数据
router.register('permission/admins', admin.AdminViewSet, base_name='admins')

# 品牌表管理
# 注意：必须写在goods路由规则的上面
router.register('goods/brands', brands.BrandViewSet, base_name='brands')

# 查询获取SPU表列表数据
router.register('goods', spu.SpuViewSet, base_name='goods')

# 规格选项表管理
router.register('specs/options', spec.SpecOptionViewSet, base_name='options')

urlpatterns += router.urls
