from rest_framework.routers import DefaultRouter
from .views import WarcViewSet, CollectionViewSet

router = DefaultRouter()
router.register(r'warcs', WarcViewSet, base_name="warc")
router.register(r'collections', CollectionViewSet, base_name="collection")
urlpatterns = router.urls
