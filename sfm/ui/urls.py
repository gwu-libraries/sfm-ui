from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
                       url(r'^$', views.HomeView.as_view(), name="home"),

                       url(r'^collections/create/$',
                           views.CollectionCreateView.as_view(),
                           name="collection_create"),

                       url(r'^collections/(?P<pk>\d+)/update/$',
                           views.CollectionUpdateView.as_view(),
                           name="collection_update"),

                       url(r'^collections/(?P<pk>\d+)/delete/$',
                           views.CollectionDeleteView.as_view(),
                           name="collection_delete"),

                       url(r'^collections/(?P<pk>\d+)/stats/(?P<item>.+?)/(?P<period>.*)/$',
                           views.collection_stats,
                           name='collection_stats'),

                       url(r'^collections/(?P<pk>\d+)/$',
                           views.CollectionDetailView.as_view(),
                           name="collection_detail"),

                       url(r'^collections/$',
                           views.CollectionListView.as_view(),
                           name="collection_list"),

                       url(r'^seedsets/(?P<collection_pk>\d+)/(?P<harvest_type>.+)/create/$',
                           views.SeedSetCreateView.as_view(),
                           name="seedset_create"),

                       url(r'^seedsets/(?P<pk>\d+)/update/$',
                           views.SeedSetUpdateView.as_view(),
                           name="seedset_update"),

                       url(r'^seedsets/(?P<pk>\d+)/toggle/$',
                           views.SeedSetToggleActiveView.as_view(),
                           name="seedset_toggle_active"),

                       url(r'^seedsets/(?P<pk>\d+)/delete/$',
                           views.SeedSetDeleteView.as_view(),
                           name="seedset_delete"),

                       url(r'^seedsets/(?P<pk>\d+)/$',
                           views.SeedSetDetailView.as_view(),
                           name="seedset_detail"),

                       url(r'^seedsets/(?P<pk>\d+)/harvests/$',
                           views.HarvestListView.as_view(),
                           name="seedset_harvests"),

                       url(r'^seeds/create/(?P<seed_set_pk>\d+)$',
                           views.SeedCreateView.as_view(),
                           name="seed_create"),

                       url(r'^seeds/bulk/(?P<seed_set_pk>\d+)$',
                           views.BulkSeedCreateView.as_view(),
                           name="bulk_seed_create"),

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

                       url(r'^credentials/(?P<platform>.+)/create/$',
                           views.CredentialCreateView.as_view(),
                           name="credential_create"),

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
                           name='export_file'),

                       url(r'^harvests/(?P<pk>\d+)/$',
                           views.HarvestDetailView.as_view(),
                           name="harvest_detail"),

                       url(r'^(?P<model>\w+)/(?P<item_id>\d+)/changes/$',
                           views.ChangeLogView.as_view(),
                           name="change_log"),
                       )
