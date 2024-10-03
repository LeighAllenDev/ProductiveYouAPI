from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPaginstaion(PageNumberPagination):
    page_size = 12
    page_query_param = 'page_size'
    max_page_size = 99

    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
        })