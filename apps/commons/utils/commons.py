import math as m
import operator
import os
import uuid
from functools import reduce

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from functools import reduce

RADIUS_OF_EARTH = 6371


class SearchFilter(object):
    # The URL query parameter used for the search.
    search_param = 'search'
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
    }
    search_title = _('Search')
    search_description = _('A search term.')

    def get_search_fields(self, view, request):
        """
        Search fields are obtained from the view, but the request is always
        passed to this method. Sub-classes can override this method to
        dynamically change the search fields based on request content.
        """
        return getattr(view, 'search_fields', None)

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.GET.get(self.search_param, '')
        return params.replace(',', ' ').split()

    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = 'icontains'
        return '__'.join([field_name, lookup])

    def must_call_distinct(self, queryset, search_fields):
        """
        Return True if 'distinct()' should be used to query the given lookups.
        """
        for search_field in search_fields:
            opts = queryset.model._meta
            if search_field[0] in self.lookup_prefixes:
                search_field = search_field[1:]
            # Annotated fields do not need to be distinct
            if isinstance(queryset, models.QuerySet) and search_field in queryset.query.annotations:
                return False
            parts = search_field.split('__')
            for part in parts:
                field = opts.get_field(part)
                if hasattr(field, 'get_path_info'):
                    # This field is a relation, update opts to follow the relation
                    path_info = field.get_path_info()
                    opts = path_info[-1].to_opts
                    if any(path.m2m for path in path_info):
                        # This field is a m2m relation so we know we need to call distinct
                        return True
        return False

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(search_field)
            for search_field in search_fields
        ]

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            if settings.DATABASES[queryset.db]["ENGINE"] == "django.db.backends.oracle":
                # distinct analogue for Oracle users
                return base.filter(pk__in=set(queryset.values_list('pk', flat=True)))
            return queryset.distinct()
        return queryset


def inverse_mapping(mapping):
    """
    Inverse key -> value to value -> key
    # NOTE: make sure values are unique
    """
    return mapping.__class__(map(reversed, mapping.items()))


def validate_coordinate(coordinate_from: tuple, coordinate_to: tuple, _range=5):
    """
    To check whether coordinate are within range or not.

    Coordinates must be tuple where fist item of tuple denotes latitude and
    second item denotes longitude for that given coordinate.
    i.e. coordinate_from = (latitude, longitude)
    """
    distance_latitude = m.radians(coordinate_to[0] - coordinate_from[0])
    distance_longitude = m.radians(coordinate_to[1] - coordinate_from[1])

    temp_distance = m.sin(distance_latitude / 2) ** 2 + m.cos(m.radians(coordinate_from[0])) ** \
                    m.cos(m.radians(coordinate_to[0])) * m.sin(distance_longitude / 2) ** 2
    computed_distance = 2 * m.sin(m.sqrt(temp_distance))
    actual_distance = RADIUS_OF_EARTH * computed_distance

    return actual_distance <= _range


def get_uuid_filename(filename):
    """
    rename the file name to uuid4 and return the
    path
    """
    ext = filename.split('.')[-1]
    return "{}.{}".format(uuid.uuid4().hex, ext)


def get_upload_path(instance, filename):
    return os.path.join(f'uploads/{instance.__class__.__name__.lower()}', get_uuid_filename(filename))


def nested_getattr(instance: object, name: str, separator='.', default=None, call=True):
    attrs = name.split(separator)
    attrs.insert(0, instance)
    try:
        attr = reduce(
            lambda instance_, attribute_: getattr(instance_, attribute_),
            attrs
        )
        if call and callable(attr):
            return attr()
        return attr
    except AttributeError:
        return default
