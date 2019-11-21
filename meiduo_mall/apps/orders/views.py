import json
from decimal import Decimal
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views import View
from django_redis import get_redis_connection

from apps.areas.models import Address
from apps.goods.models import SKU
from apps.orders.models import OrderInfo, OrderGoods
from utils.response_code import RETCODE


# 详情页展示评价信息
class OrderCommentInfoView(View):
    """详情页展示评价信息"""
    def get(self, request, sku_id):
        # 校验参数
        if not sku_id:
            return http.HttpResponseForbidden('参数sku_id不存在')
        try:
            order_goods_list = OrderGoods.objects.filter(sku_id=sku_id, is_commented=True).order_by('-create_time')[:30]
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('参数sku_id错误')
        # 构建商品评价数据
        comment_list = []
        for order_goods in order_goods_list:
            username = order_goods.order.user.username
            comment_list.append({
                'username': username[0] + '***' + username[-1] if order_goods.is_anonymous else username,
                'comment': order_goods.comment,
                'score': order_goods.score,
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'comment_list': comment_list})


# 展示商品评价页面
class OrderCommentView(LoginRequiredMixin, View):
    """展示商品评价页面"""
    def get(self, request):
        # 接收参数
        order_id = request.GET.get('order_id')
        # 校验参数
        try:
            OrderInfo.objects.get(order_id=order_id, user=request.user)
        except OrderInfo.DoesNotExist:
            return http.HttpResponseNotFound('订单不存在')

        # 查询未评价商品信息
        try:
            uncomment_goods = OrderGoods.objects.filter(order_id=order_id, is_commented=False)
        except Exception:
            return http.HttpResponseServerError('订单商品信息出错')

        # 构建待评价商品数据
        uncomment_goods_list = []
        for goods in uncomment_goods:
            uncomment_goods_list.append({
                'order_id': goods.order.order_id,
                'sku_id': goods.sku.id,
                'name': goods.sku.name,
                'price': str(goods.price),
                'default_image_url': goods.sku.default_image.url,
                'comment': goods.comment,
                'score': goods.score,
                'is_anonymous': str(goods.is_anonymous),
            })

        # 渲染模板
        context = {'uncomment_goods_list': uncomment_goods_list}

        return render(request, 'goods_judge.html', context)

    # 评价订单商品
    def post(self, request):
        """评价订单商品"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        order_id = json_dict.get('order_id')
        sku_id = json_dict.get('sku_id')
        score = json_dict.get('score')
        comment = json_dict.get('comment')
        is_anonymous = json_dict.get('is_anonymous')

        # 校验参数
        if not all([order_id, order_id, sku_id, score, comment]):
            return http.HttpResponseForbidden('缺少必传参数')

        try:
            OrderInfo.objects.filter(order_id=order_id, user=request.user, status=OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('参数order_id错误')

        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('参数sku_id错误')

        if is_anonymous:
            if not isinstance(is_anonymous, bool):
                return http.HttpResponseForbidden('参数is_anonymous错误')

        # 保存订单信息
        OrderGoods.objects.filter(order_id=order_id, sku_id=sku_id, is_commented=False).update(
            comment=comment,
            score=score,
            is_anonymous=is_anonymous,
            is_commented=True,
        )

        # 累计评论数据
        sku.comments += 1
        sku.save()
        sku.spu.comments += 1
        sku.spu.save()
        # 如果所有订单商品都已评价，则修改订单状态为已完成
        if OrderGoods.objects.filter(order_id=order_id, is_commented=False).count() == 0:
            OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM['FINISHED'])

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '评价成功'})


# 我的订单
class OrderInfoView(LoginRequiredMixin, View):
    """我的订单"""
    def get(self, request, page_num):
        # 获取登陆用户
        user = request.user
        # 查询用户的所有订单
        orders = user.orderinfo_set.all().order_by('-create_time')
        # 遍历订单
        for order in orders:
            # 订单状态
            order.status_name = OrderInfo.ORDER_STATUS_CHOICES[order.status - 1][1]
            # 支付方式
            order.pay_method_name = OrderInfo.PAY_METHOD_CHOICES[order.pay_method - 1][1]
            order.sku_list = []
            # 查询订单商品
            order_goods = order.skus.all()
            # 遍历所有商品
            for order_good in order_goods:
                sku = order_good.sku
                sku.count = order_good.count
                sku.amount = sku.price * sku.count
                order.sku_list.append(sku)

        #  分页
        page_num = int(page_num)
        try:
            paginator = Paginator(orders, 5)
            page_orders = paginator.page(page_num)
            total_page = paginator.num_pages
        except Exception as e:
            return http.HttpResponseNotFound('订单不存在')

        context = {
            # 每页显示的内容
            "page_orders": page_orders,
            # 总页数
            'total_page': total_page,
            # 当前页
            'page_num': page_num,
        }

        return render(request, 'user_center_order.html', context)


# 提交订单成功
class OrderSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        """提交订单成功"""
        # 接收参数
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')

        # 修改为前端数据格式
        context = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method
        }
        return render(request, 'order_success.html', context)


#  提交订单
class OrderCommitView(LoginRequiredMixin, View):
    """订单提交"""
    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 获取当前要保存的订单数据
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')

        # 校验参数
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断address_id 是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Exception:
            return http.HttpResponseForbidden('参数address_id错误')

        # 判断pay_method 是否合法
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return http.HttpResponseForbidden('参数pay_method错误')

        # 显式的开启一个事务
        from django.db import transaction
        # --------设置事物起始--------
        with transaction.atomic():

            # --------事物保存点--------
            save_id = transaction.savepoint()

            try:
                # 获取登录用户
                user = request.user
                # 生成订单编号：年月日时分秒+用户编号
                order_id = datetime.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

                # 保存订单基本信息 OrderInfo（一）
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )

                # 从购物车 取出选中的商品
                client = get_redis_connection('carts')
                carts_data = client.hgetall(user.id)
                carts_dict = {}
                for key, value in carts_data.items():
                    sku_id = key
                    sku_dict = json.loads(value.decode())
                    if sku_dict['selected']:
                        carts_dict[sku_id] = sku_dict

                # 遍历 商品信息
                sku_ids = carts_dict.keys()
                for sku_id in sku_ids:

                    while True:
                        sku = SKU.objects.get(id=sku_id)

                        # 原始销量 和  库存量
                        origin_sales = sku.sales
                        origin_stock = sku.stock

                        # 判断货源是否充足
                        cart_count = carts_dict[sku_id]['count']
                        if cart_count > sku.stock:

                            # --------事物回滚--------
                            transaction.savepoint_rollback(save_id)
                            return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

                        # 延迟测试 bug
                        # import time
                        # time.sleep(10)

                        # sku减少库存, 增加销量
                        # sku.stock -= cart_count
                        # sku.sales += cart_count
                        # sku.save()

                        # 使用乐观锁 更新库存量
                        new_stock = origin_stock - cart_count
                        new_sales = origin_sales + cart_count
                        result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)
                        # 如果下单下单失败,库存足够则继续下单,直到下单成功或者库存不足
                        if result == 0:
                            continue

                        # SPU 增加销量
                        sku.spu.sales += cart_count
                        sku.spu.save()

                        # 保存订单商品信息
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=cart_count,
                            price=sku.price,
                        )

                        # 保存商品订单中总价和总数量
                        order.total_count += cart_count
                        order.total_amount += (cart_count * sku.price)

                        # 下单成功 或失败跳出
                        break

                # 添加邮费和保存订单
                order.total_amount += order.freight
                order.save()

            except Exception as e:

                # --------事物回滚--------
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单失败'})

            # --------提交事物--------
            transaction.savepoint_commit(save_id)

        # 清除购物车已经结算过的商品
        client.hdel(user.id, *carts_dict)

        # 返回响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})


# 结算订单页面显示
class OrderSettlementView(LoginRequiredMixin, View):
    def get(self, request):
        """提供订单结算页面"""
        # 获取登录用户
        user = request.user

        # 查询地址
        try:
            addresses = Address.objects.filter(user=user, is_deleted=False)
        except:
            # 如果地址为空，渲染模板时会判断，并跳转到地址编辑页面
            addresses = None

        # 查询选中的商品
        client = get_redis_connection('carts')
        carts_data = client.hgetall(user.id)
        # 转换格式
        carts_dict = {}
        for key, value in carts_data.items():
            sku_id = int(key.decode())
            sku_dict = json.loads(value.decode())
            if sku_dict['selected']:
                carts_dict[sku_id] = sku_dict

        # 计算金额和邮费
        total_count = 0
        total_amount = Decimal(0.00)

        skus = SKU.objects.filter(id__in=carts_dict.keys())
        for sku in skus:
            sku.count = carts_dict[sku.id].get('count')
            sku.amount = sku.count * sku.price

            # 计算总数量和金额
            total_count += sku.count
            total_amount += sku.amount

        # 运费
        freight = Decimal('10.00')

        # 转换前端数据格式
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight,
            'default_address_id': user.default_address_id
        }

        return render(request, 'place_order.html', context)
