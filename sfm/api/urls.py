from rest_framework.routers import DefaultRouter
from .views import WarcViewSet

router = DefaultRouter()
router.register(r'warcs', WarcViewSet, base_name="warc")
urlpatterns = router.urls