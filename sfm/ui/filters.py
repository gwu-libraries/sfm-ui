import django_filters
from django.db.models.query_utils import Q

from .models import Seed, Collection, CollectionSet


class SeedFilter(django_filters.FilterSet):
    search = django_filters.MethodFilter(action="filter_search")

    class Meta:
        model = Seed
        fields = ('search',)

    def filter_search(self, queryset, value):
        return queryset.filter(Q(token__icontains=value) | Q(uid__icontains=value))


class CollectionFilter(django_filters.FilterSet):
    search = django_filters.MethodFilter(action="filter_search")

    class Meta:
        model = Collection
        fields = ('search',)

    def filter_search(self, queryset, value):
        return queryset.filter(Q(name__icontains=value))


class CollectionSetFilter(django_filters.FilterSet):
    search = django_filters.MethodFilter(action="filter_search")

    class Meta:
        model = CollectionSet
        fields = ('search',)

    def filter_search(self, queryset, value):
        return queryset.filter(Q(name__icontains=value))