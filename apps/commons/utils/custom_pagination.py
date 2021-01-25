from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1


class CustomPagination(LimitOffsetPagination):
    page = DEFAULT_PAGE
    default_limit = 10
    page_size_query_param = 'page_size'

    def __init__(self):
        (self.count, self.limit, self.request, self.offset) = (0, 0, None, 0)

    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        try:
            self.limit = int(request.query_params.get('limit', self.count))
        except (TypeError, ValueError):
            self.limit = self.count
        if self.limit is None:
            self.limit = self.count

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data):
        offset = self.request.query_params.get('offset')
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.count,
            'offset': offset,
            'results': data
        })
