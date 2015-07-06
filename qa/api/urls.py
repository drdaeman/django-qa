from __future__ import absolute_import
from django.conf.urls import patterns, url, include
from rest_framework import routers
from .views import UserViewSet, QuestionViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'^users', UserViewSet)
router.register(r'^questions', QuestionViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
