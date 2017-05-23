from rest_framework.serializers import HyperlinkedModelSerializer
from ui.models import Warc, Collection


class WarcSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Warc
        fields = ('warc_id', 'path', 'sha1', 'bytes', 'date_created', 'harvest_type')


class CollectionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = ('collection_id', 'harvest_type', 'name', 'is_on')
