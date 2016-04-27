from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',

                       url(r'^collections/create/$',
                           views.CollectionCreateView.as_view(),
                           name="collection_create"),

                       url(r'^collections/(?P<pk>\d+)/update/$',
                           views.CollectionUpdateView.as_view(),
                           name="collection_update"),

                       url(r'^collections/(?P<pk>\d+)/delete/$',
                           views.CollectionDeleteView.as_view(),
                           name="collection_delete"),

                       url(r'^collections/(?P<pk>\d+)/$',
                           views.CollectionDetailView.as_view(),
                           name="collection_detail"),

                       url(r'^collections/$',
                           views.CollectionListView.as_view(),
                           name="collection_list"),

                       url(r'^seedsets/create/(?P<collection_pk>\d+)$',
                           views.SeedSetCreateView.as_view(),
                           name="seedset_create"),

                       url(r'^seedsets/(?P<pk>\d+)/update/(?P<collection_pk>\d+)$',
                           views.SeedSetUpdateView.as_view(),
                           name="seedset_update"),

                       url(r'^seedsets/(?P<pk>\d+)/delete/$',
                           views.SeedSetDeleteView.as_view(),
                           name="seedset_delete"),

                       url(r'^seedsets/(?P<pk>\d+)/$',
                           views.SeedSetDetailView.as_view(),
                           name="seedset_detail"),

                       url(r'^seeds/create/(?P<seed_set_pk>\d+)$',
                           views.SeedCreateView.as_view(),
                           name="seed_create"),

                       url(r'^seeds/(?P<pk>\d+)/update/$',
                           views.SeedUpdateView.as_view(),
                           name="seed_update"),

                       url(r'^seeds/(?P<pk>\d+)/delete/$',
                           views.SeedDeleteView.as_view(),
                           name="seed_delete"),

                       url(r'^seeds/(?P<pk>\d+)/$',
                           views.SeedDetailView.as_view(),
                           name="seed_detail"),

                       url(r'^seeds/$',
                           views.SeedListView.as_view(),
                           name="seed_list"),

                       url(r'^credentials/(?P<pk>\d+)/$',
                           views.CredentialDetailView.as_view(),
                           name="credential_detail"),

                       url(r'^credentials/twitter/create/$',
                           views.CredentialTwitterCreateView.as_view(),
                           name="credential_twitter_create"),

                       url(r'^credentials/weibo/create/$',
                           views.CredentialWeiboCreateView.as_view(),
                           name="credential_weibo_create"),

                       url(r'^credentials/flickr/create/$',
                           views.CredentialFlickrCreateView.as_view(),
                           name="credential_flickr_create"),

                       url(r'^credentials/(?P<pk>\d+)/update/$',
                           views.CredentialUpdateView.as_view(),
                           name="credential_update"),

                       url(r'^credentials/$',
                           views.CredentialListView.as_view(),
                           name="credential_list"),

                       url(r'^exports/$',
                           views.ExportListView.as_view(),
                           name="export_list"),

                       url(r'^exports/create/(?P<seedset_pk>\d+)$',
                           views.ExportCreateView.as_view(),
                           name="export_create"),

                       url(r'^exports/(?P<pk>\d+)/$',
                           views.ExportDetailView.as_view(),
                           name="export_detail"),

                       url(r'^exports/(?P<pk>\d+)/file/(?P<file_name>.*)$',
                           views.export_file,
                           name='export_file')
                       )
