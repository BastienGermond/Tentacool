from django.urls import path, include, re_path

from rest_framework import routers

from backend.views import BlobViewSet

router = routers.SimpleRouter()
# router.register(r'blobs/(?P<filename>[^/]+)$', BlobViewSet.as_view())

urlpatterns = [
    re_path(r'^blobs/(?P<filename>.+)$', BlobViewSet.as_view()),

    path('', include(router.urls)),
]
