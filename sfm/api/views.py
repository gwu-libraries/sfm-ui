from rest_framework.viewsets import ReadOnlyModelViewSet
from ui.models import Warc
from .serializers import WarcSerializer
from .filters import WarcFilter


class WarcViewSet(ReadOnlyModelViewSet):
    serializer_class = WarcSerializer
    lookup_field = "warc_id"
    filter_fields = ('warc_id', 'path')
    filter_class = WarcFilter

    def get_queryset(self):
        return Warc.objects.all()
