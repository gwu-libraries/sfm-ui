from django_filters import FilterSet, CharFilter, IsoDateTimeFilter, MethodFilter
from ui.models import Warc, Seed, Harvest, Collection
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
    exclude_web = MethodFilter(action="web_filter")

    class Meta:
        model = Warc
        fields = ['collection']

    @staticmethod
    def web_filter(queryset, value):
        if value.lower() in ("true", "yes"):
            return queryset.exclude(harvest__harvest_type='web')
        else:
            return queryset


class CollectionFilter(FilterSet):
    collection_startswith = CharFilter(name="collection_id", lookup_type="istartswith")

    class Meta:
        model = Collection