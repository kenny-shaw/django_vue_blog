# 分页
# 引入分页模块
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    # max_page_size = 10
    page_query_param = 'page'
