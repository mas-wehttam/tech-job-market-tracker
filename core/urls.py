from django.urls import path, include
from . import views
from . import api_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('jobposts', api_views.JobPostViewset, basename='jobpost')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('dashboard/', views.job_dashboard, name='dashboard'),
]


