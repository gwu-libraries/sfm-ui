from django.conf.urls import patterns, url
from .views import (CollectionListView, CollectionCreateView,
                    CollectionDetailView, CollectionUpdateView,
                    CollectionDeleteView)
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',

                       url(r'^collections/create/$',  # NOQA
                           login_required(CollectionCreateView.as_view()),
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
                       )
