from django.conf.urls import patterns, url
from .views import (CollectionListView, CollectionCreateView,
                    CollectionDetailView, CollectionUpdateView,
                    CollectionDeleteView, SeedSetListView,
                    SeedSetCreateView, SeedSetDetailView,
                    SeedSetUpdateView, SeedSetDeleteView,
                    SeedListView, SeedCreateView, SeedDetailView,
                    SeedUpdateView, SeedDeleteView)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


urlpatterns = patterns('',

                       url(r'^collections/create/$',
                           login_required(CollectionCreateView.as_view(
                               success_url=reverse_lazy('collection_list'))),
                           name="collection_create"),

                       url(r'^collections/(?P<pk>\d+)/update/$',
                           login_required(CollectionUpdateView.as_view()),
                           name="collection_update"),

                       url(r'^collections/(?P<pk>\d+)/delete/$',
                           login_required(CollectionDeleteView.as_view()),
                           name="collection_delete"),

                       url(r'^collections/(?P<pk>\d+)/$',
                           CollectionDetailView.as_view(),
                           name="collection_detail"),

                       url(r'^collections/$',
                           CollectionListView.as_view(),
                           name="collection_list"),

                       url(r'^seedsets/create/$',
                           login_required(SeedSetCreateView.as_view(
                               success_url=reverse_lazy('seedset_list'))),
                           name="seedset_create"),

                       url(r'^seedsets/(?P<pk>\d+)/update/$',
                           login_required(SeedSetUpdateView.as_view()),
                           name="seedset_update"),

                       url(r'^seedsets/(?P<pk>\d+)/delete/$',
                           login_required(SeedSetDeleteView.as_view()),
                           name="seedset_delete"),

                       url(r'^seedsets/(?P<pk>\d+)/$',
                           SeedSetDetailView.as_view(),
                           name="seedset_detail"),

                       url(r'^seedsets/$',
                           SeedSetListView.as_view(),
                           name="seedset_list"),

                       url(r'^seeds/create/$',
                           login_required(SeedCreateView.as_view(
                               success_url=reverse_lazy('seed_list'))),
                           name="seed_create"),

                       url(r'^seeds/(?P<pk>\d+)/update/$',
                           login_required(SeedUpdateView.as_view()),
                           name="seed_update"),

                       url(r'^seeds/(?P<pk>\d+)/delete/$',
                           login_required(SeedDeleteView.as_view()),
                           name="seed_delete"),

                       url(r'^seeds/(?P<pk>\d+)/$',
                           SeedDetailView.as_view(),
                           name="seed_detail"),

                       url(r'^seeds/$',
                           SeedListView.as_view(),
                           name="seed_list"),
                       )
