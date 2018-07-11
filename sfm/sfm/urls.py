from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from .views import password_reset_done

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="ui/", permanent=True)),
    url(r'^admin/', admin.site.urls),
    url(r"^accounts/password/reset/done/$", password_reset_done, name="account_reset_password_done"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ui/', include('ui.urls')),
    url(r'^api/v1/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls'))
]
