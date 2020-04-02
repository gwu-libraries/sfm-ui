from rest_framework.routers import DefaultRouter
from .views import WarcViewSet, CollectionViewSet

router = DefaultRouter()
router.register(r'warcs', WarcViewSet, basename="warc")
router.register(r'collections', CollectionViewSet, basename="collection")
urlpatterns = router.urls
