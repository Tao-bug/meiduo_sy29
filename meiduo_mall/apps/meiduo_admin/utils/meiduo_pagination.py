from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MeiduoPagination(PageNumberPagination):
    # 默认后端指定每页显示数量
    page_size = 10
    # 允许查询参数接收page_size参数， 用于指定每页大小
    page_size_query_param = 'pagesize'
    # 超过此值的时候， 每页显示此值大小
    max_page_size = 100

    # 重写分页返回结果  按照指定的字段进行分页数据返回
    def get_paginated_response(self, data):
        return Response({
            "counts": self.page.paginator.count,  # 总数量
            "lists": data,  # 用户数据
            "page": self.page.number,  # 当前页数
            "pages": self.page.paginator.num_pages,  # 总页数
            "pagesize": self.page.paginator.per_page  # 后端指定的页容量
        })
