from rest_framework.viewsets import ReadOnlyModelViewSet
from ui.models import Warc, Collection
from .serializers import WarcSerializer, CollectionSerializer
from .filters import WarcFilter, CollectionFilter


class WarcViewSet(ReadOnlyModelViewSet):
    serializer_class = WarcSerializer
    lookup_field = "warc_id"
    filter_fields = ('warc_id', 'path')
    filter_class = WarcFilter

    def get_queryset(self):
        return Warc.objects.all()


class CollectionViewSet(ReadOnlyModelViewSet):
    serializer_class = CollectionSerializer
    lookup_field = "warc_id"
    filter_class = CollectionFilter

    def get_queryset(self):
        return Collection.objects.all()