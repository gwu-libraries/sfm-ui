from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="ui/", permanent=True)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ui/', include('ui.urls')),
    url(r'^api/v1/', include('api.urls')),
]
