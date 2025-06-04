from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsortiumMemberViewSet, ExpertViewSet, TAFRecordViewSet

router = DefaultRouter()
router.register(r'consortium-members', ConsortiumMemberViewSet)
router.register(r'experts', ExpertViewSet)
router.register(r'taf-records', TAFRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
