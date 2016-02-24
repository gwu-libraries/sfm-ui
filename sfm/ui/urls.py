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

                       url(r'^seedsets/(?P<pk>\d+)/update/$',
                           views.SeedSetUpdateView.as_view(),
                           name="seedset_update"),

                       url(r'^seedsets/(?P<pk>\d+)/delete/$',
                           views.SeedSetDeleteView.as_view(),
                           name="seedset_delete"),

                       url(r'^seedsets/(?P<pk>\d+)/$',
                           views.SeedSetDetailView.as_view(),
                           name="seedset_detail"),

                       url(r'^seedsets/$',
                           views.SeedSetListView.as_view(),
                           name="seedset_list"),

                       url(r'^seeds/create/$',
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

                       url(r'^credentials/create/$',
                           views.CredentialCreateView.as_view(),
                           name="credential_create"),

                       url(r'^credentials/$',
                           views.CredentialListView.as_view(),
                           name="credential_list"),
                       )
