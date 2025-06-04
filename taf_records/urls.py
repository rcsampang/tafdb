from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConsortiumMemberViewSet, ExpertViewSet, TAFRecordViewSet,
    TriggerBackupDatabaseAPIView, TriggerBackupApplicationAPIView,
    ListBackupsAPIView, DownloadBackupAPIView
)

router = DefaultRouter()
router.register(r'consortium-members', ConsortiumMemberViewSet)
router.register(r'experts', ExpertViewSet)
router.register(r'taf-records', TAFRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('backups/trigger/database/', TriggerBackupDatabaseAPIView.as_view(), name='backup-trigger-database'),
    path('backups/trigger/application/', TriggerBackupApplicationAPIView.as_view(), name='backup-trigger-application'),
    path('backups/list/', ListBackupsAPIView.as_view(), name='backup-list'),
    path('backups/download/<str:type>/<str:filename>/', DownloadBackupAPIView.as_view(), name='backup-download'),
]
