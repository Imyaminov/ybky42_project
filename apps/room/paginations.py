from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class RoomListPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'count': self.page.paginator.count,
            'page_size': len(self.page),
            'results': data
        })
