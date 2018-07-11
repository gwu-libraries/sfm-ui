from django_filters import FilterSet, CharFilter, IsoDateTimeFilter
from ui.models import Warc, Collection
from django_filters import Filter
from django_filters.fields import Lookup


class ListFilter(Filter):
    def filter(self, qs, value):
        return super(ListFilter, self).filter(qs, Lookup(value.split(u","), "in"))


class WarcFilter(FilterSet):
    # Allows queries like /api/v1/warcs/?collection=39c00280274a4db0b1cb5bfa4d527a1e
    collection = CharFilter(name="harvest__historical_collection__collection_id")
    seed = ListFilter(name="harvest__historical_seeds__seed_id", distinct=True)
    harvest_date_start = IsoDateTimeFilter(name="harvest__date_started", lookup_type='gte')
    harvest_date_end = IsoDateTimeFilter(name="harvest__date_started", lookup_type='lte')
    created_date_start = IsoDateTimeFilter(name="date_created", lookup_type='gte')
    created_date_end = IsoDateTimeFilter(name="date_created", lookup_type='lte')

    class Meta:
        model = Warc
        fields = ['collection']


class CollectionFilter(FilterSet):
    collection_startswith = CharFilter(name="collection_id", lookup_type="istartswith")

    class Meta:
        model = Collection
        fields = ['collection_set']