from celery_tasks.main import app
import os
# 千万注意 --项目的包 在 最下面
from apps.contents.utils import get_categories
from apps.goods.utils import get_breadcrumb
from django.template import loader
from django.conf import settings
from apps.goods.models import SKU


def generate_static_sku_detail_html(sku):
    # 1.detai_data
    # 查询商品频道分类
    categories = get_categories()
    # 查询面包屑导航
    breadcrumb = get_breadcrumb(sku.category)

    # 构建当前商品的规格键
    sku_specs = sku.specs.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        sku_key.append(spec.option.id)
    # 获取当前商品的所有SKU
    skus = sku.spu.sku_set.all()
    # 构建不同规格参数（选项）的sku字典
    spec_sku_map = {}
    for s in skus:
        # 获取sku的规格参数
        s_specs = s.specs.order_by('spec_id')
        # 用于形成规格参数-sku字典的键
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        # 向规格参数-sku字典添加记录
        spec_sku_map[tuple(key)] = s.id
    # 获取当前商品的规格信息
    goods_specs = sku.spu.specs.order_by('id')
    # 若当前sku的规格信息不完整，则不再继续
    if len(sku_key) < len(goods_specs):
        return
    for index, spec in enumerate(goods_specs):
        # 复制当前sku的规格键
        key = sku_key[:]
        # 该规格的选项
        spec_options = spec.options.all()
        for option in spec_options:
            # 在规格参数sku字典中查找符合当前规格的sku
            key[index] = option.id
            option.sku_id = spec_sku_map.get(tuple(key))
        spec.spec_options = spec_options

    # 渲染页面
    context = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs,
    }

    # 2.detail_template_file
    template_file = loader.get_template('detail.html')

    # 3.render
    html_text = template_file.render(context)

    # 4.写入本地
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'detail/{}.html'.format(sku.id))
    with open(file_path, 'w') as f:
        f.write(html_text)


@app.task(bind=True, name="task_generate", retry_backoff=10)
def task_generate(self, sku_id):
    try:
        sku = SKU.objects.get(pk=sku_id)
        generate_static_sku_detail_html(sku)
    except Exception as e:
        raise self.retry(exc=e, max_retries=3)
