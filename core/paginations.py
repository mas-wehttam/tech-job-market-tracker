from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 15 # Default page size
    page_size_query_param = 'page_size' # Shows page_size=5
    page_query_param = 'page-num' # Shows page-num=1
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.get_page_size(self.request),
            'results': data,
        })