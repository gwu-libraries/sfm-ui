from django_filters import rest_framework as filters
from ui.models import Warc, Collection
from django_filters.widgets import CSVWidget


class ListFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class WarcFilter(filters.FilterSet):
    # Allows queries like /api/v1/warcs/?collection=39c00280274a4db0b1cb5bfa4d527a1e
    collection = filters.CharFilter(field_name="harvest__historical_collection__collection_id")
    seed = ListFilter(widget=CSVWidget, field_name="harvest__historical_seeds__seed_id", distinct=True, lookup_expr='in') 
    harvest_date_start = filters.IsoDateTimeFilter(field_name="harvest__date_started", lookup_expr='gte')
    harvest_date_end = filters.IsoDateTimeFilter(field_name="harvest__date_started", lookup_expr='lte')
    created_date_start = filters.IsoDateTimeFilter(field_name="date_created", lookup_expr='gte')
    created_date_end = filters.IsoDateTimeFilter(field_name="date_created", lookup_expr='lte')

    class Meta:
        model = Warc
        fields = ['collection']


class CollectionFilter(filters.FilterSet):
    collection_startswith = filters.CharFilter(field_name="collection_id", lookup_expr="istartswith")

    class Meta:
        model = Collection
        fields = ['collection_set']
