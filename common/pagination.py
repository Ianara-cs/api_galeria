from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomQueryPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        # Se "is_page" for diferente de "true", desativa a paginação
        is_page = request.query_params.get('is_page', '').lower()
        if is_page != 'true':
            self._no_pagination = True
            return None
        self._no_pagination = False
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if getattr(self, '_no_pagination', False):
            return Response({
                "is_page": False,
                "results": data
            })
        return Response({
            "page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "count": self.page.paginator.count,
            "num_pages": self.page.paginator.num_pages,
            "results": data
        })

