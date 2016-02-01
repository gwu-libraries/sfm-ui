from rest_framework.serializers import HyperlinkedModelSerializer
from ui.models import Warc


class WarcSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Warc
        fields = ('warc_id', 'path', 'sha1', 'bytes', 'date_created')