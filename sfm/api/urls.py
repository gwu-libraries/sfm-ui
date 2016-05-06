from rest_framework.routers import DefaultRouter
from .views import WarcViewSet, SeedSetViewSet

router = DefaultRouter()
router.register(r'warcs', WarcViewSet, base_name="warc")
router.register(r'seedsets', SeedSetViewSet, base_name="seedset")
urlpatterns = router.urls