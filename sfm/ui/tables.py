# coding: utf-8
import django_tables2 as tables
from django.utils.html import mark_safe
from .models import Seed
from django_tables2.utils import A
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
