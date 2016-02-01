from django_filters import FilterSet, CharFilter, IsoDateTimeFilter
from ui.models import Warc, Seed, Harvest
from django_filters import Filter
from django_filters.fields import Lookup


class ListFilter(Filter):
    def filter(self, qs, value):
        return super(ListFilter, self).filter(qs, Lookup(value.split(u","), "in"))


class WarcFilter(FilterSet):
    # Allows queries like /api/v1/warcs/?seedset=39c00280274a4db0b1cb5bfa4d527a1e
    seedset = CharFilter(name="harvest__seed_set__seedset_id")
    seed = ListFilter(name="harvest__seed_set__seeds__seed_id", distinct=True)
    # TODO: This will need to be changed to use historical seeds once #54 is completed.
    harvest_date_start = IsoDateTimeFilter(name="harvest__date_started", lookup_type='gte')
    harvest_date_end = IsoDateTimeFilter(name="harvest__date_started", lookup_type='lte')

    class Meta:
        model = Warc
        fields = ['seedset']
