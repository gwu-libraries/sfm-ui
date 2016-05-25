from rest_framework.serializers import HyperlinkedModelSerializer
from ui.models import Warc, SeedSet


class WarcSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Warc
        fields = ('warc_id', 'path', 'sha1', 'bytes', 'date_created', 'harvest_type')


class SeedSetSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = SeedSet
        fields = ('seedset_id', 'harvest_type', 'name', 'is_active')
