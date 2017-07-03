import django_filters
from django.db.models.query_utils import Q

from .models import Seed


class SeedFilter(django_filters.FilterSet):
    search = django_filters.MethodFilter(action="filter_search")

    class Meta:
        model = Seed
        fields = ('search',)

    def filter_search(self, queryset, value):
        return queryset.filter(Q(token__icontains=value) | Q(uid__icontains=value))
