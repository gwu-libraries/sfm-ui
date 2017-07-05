# coding: utf-8
import django_tables2 as tables
from django.utils.html import mark_safe
from .models import CollectionSet, Collection, Seed, Credential, Harvest, Export, User, Warc
from django_tables2.utils import A
from django.db.models import Count, Case, When, IntegerField
from django.contrib.staticfiles.templatetags.staticfiles import static


class SeedTable(tables.Table):
    link = tables.LinkColumn(verbose_name="Link", orderable=False, empty_values=())
    token = tables.LinkColumn('seed_detail', args=[A('pk')], empty_values=())
    uid = tables.LinkColumn('seed_detail', args=[A('pk')], empty_values=())
    message = tables.Column(verbose_name="Message", orderable=False, empty_values=())

    class Meta:
        model = Seed
        attrs = {'class': 'table table-striped'}
        fields = ['link', 'token', 'uid', 'message']
        empty_text = 'No records available.'

    def __init__(self, *args, **kwargs):
        self.token_name = kwargs.pop('token_name', "token")
        self.uid_name = kwargs.pop('uid_name', "uid")
        self.platform = kwargs.pop('platform', "twitter")
        self.seed_message = kwargs.pop('msg', {})
        self.base_columns['token'].verbose_name = self.token_name
        self.base_columns['uid'].verbose_name = self.uid_name
        super(SeedTable, self).__init__(*args, **kwargs)

    def render_link(self, record):
        return mark_safe('<a target="_blank" href="{0}"> <img src="{1}" height=35 width=35/></a>'.format(
            record.social_url, static('ui/img/{}_logo.png'.format(self.platform))))

    def render_message(self, record):
        msg_seed = ""
        for msg in self.seed_message['info'].get(record.seed_id, []):
            msg_seed += '<li><p class="text-info">{}</p></li>'.format(msg)
        for msg in self.seed_message['warn'].get(record.seed_id, []):
            msg_seed += '<li><p class="text-info">{}</p></li>'.format(msg)
        for msg in self.seed_message['error'].get(record.seed_id, []):
            msg_seed += '<li><p class="text-info">{}</p></li>'.format(msg)
        return mark_safe('<ul>{}</ul>'.format(msg_seed))


class CollectionTable(tables.Table):
    name = tables.LinkColumn('collection_detail', verbose_name="Name", args=[A('pk')], empty_values=())
    harvest_type = tables.Column(verbose_name="Harvest type", empty_values=())
    active_seed = tables.Column(verbose_name='Active seeds', empty_values=())
    status = tables.Column(order_by=('is_on', 'is_active'), verbose_name="On/off/inactive", empty_values=())

    class Meta:
        model = Collection
        attrs = {'class': 'table table-striped'}
        fields = ['name', 'harvest_type', 'active_seed', 'status']
        empty_text = 'No records available.'

    def __init__(self, *args, **kwargs):
        super(CollectionTable, self).__init__(*args, **kwargs)

    def render_harvest_type(self, record):
        return record.get_harvest_type_display

    def render_active_seed(self, record):
        return record.active_seed_count

    def order_active_seed(self, queryset, is_descending):
        queryset = queryset.annotate(
            active_seed=Count(Case(
                            When(seeds__is_active=True, then=1),
                            output_field=IntegerField()))
        ).order_by(('-' if is_descending else '') + 'active_seed')
        return queryset, True

    def render_status(self, record):
        if record.status == 'On':
            status_str = mark_safe('<span class="text-success">On</span>')
        else:
            status_str = record.status
        return status_str


class CollectionSetTable(tables.Table):
    name = tables.LinkColumn('collection_set_detail', verbose_name="Name", args=[A('pk')], empty_values=())
    collections = tables.Column(verbose_name="Collections", order_by='num_collections', empty_values=())
    date_added = tables.Column(verbose_name='Date Added', empty_values=())
    group = tables.Column(verbose_name="Groups", empty_values=())

    class Meta:
        model = CollectionSet
        attrs = {'class': 'table table-striped'}
        fields = ['name', 'collections', 'date_added', 'group']
        empty_text = 'No records available.'

    def __init__(self, *args, **kwargs):
        super(CollectionSetTable, self).__init__(*args, **kwargs)

    def render_collections(self, record):
        return "{} collections".format(record.num_collections)