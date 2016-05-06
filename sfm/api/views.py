from rest_framework.viewsets import ReadOnlyModelViewSet
from ui.models import Warc, SeedSet
from .serializers import WarcSerializer, SeedSetSerializer
from .filters import WarcFilter, SeedSetFilter


class WarcViewSet(ReadOnlyModelViewSet):
    serializer_class = WarcSerializer
    lookup_field = "warc_id"
    filter_fields = ('warc_id', 'path')
    filter_class = WarcFilter

    def get_queryset(self):
        return Warc.objects.all()

class SeedSetViewSet(ReadOnlyModelViewSet):
    serializer_class = SeedSetSerializer
    lookup_field = "warc_id"
    filter_class = SeedSetFilter

    def get_queryset(self):
        return SeedSet.objects.all()