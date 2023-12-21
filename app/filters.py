# filters.py

from django_filters import rest_framework as filters
from .models import Box

class BoxFilter(filters.FilterSet):
    length_more_than = filters.NumberFilter(field_name='length', lookup_expr='gt')
    length_less_than = filters.NumberFilter(field_name='length', lookup_expr='lt')
    breadth_more_than = filters.NumberFilter(field_name='breadth', lookup_expr='gt')
    breadth_less_than = filters.NumberFilter(field_name='breadth', lookup_expr='lt')
    height_more_than = filters.NumberFilter(field_name='height', lookup_expr='gt')
    height_less_than = filters.NumberFilter(field_name='height', lookup_expr='lt')
    area_more_than = filters.NumberFilter(method='filter_area_more_than')
    area_less_than = filters.NumberFilter(method='filter_area_less_than')
    volume_more_than = filters.NumberFilter(method='filter_volume_more_than')
    volume_less_than = filters.NumberFilter(method='filter_volume_less_than')
    created_by_username = filters.CharFilter(field_name='user__username')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Box
        fields = []

    def filter_area_more_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0, area__gt=value)

    def filter_area_less_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0, area__lt=value)

    def filter_volume_more_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0, volume__gt=value)

    def filter_volume_less_than(self, queryset, name, value):
        return queryset.filter(length__gt=0, breadth__gt=0, height__gt=0, volume__lt=value)
