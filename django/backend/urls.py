"""db_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import (include, path)
from rest_framework import routers
from .api import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'archer', views.ArcherViewSet)
router.register(r'clubs', views.ClubViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'series', views.SeriesViewSet)
router.register(r'records', views.RecordViewSet)
router.register(r'events', views.EventViewSet, basename='events')
router.register(r'events/rounds', views.RoundViewSet)
router.register(r'events/descriptions', views.EventDescriptionViewSet)
router.register(r'events/participants', views.ParticipantViewSet)
router.register(r'events/participants/arrows', views.ArrowViewSet)

urlpatterns = [
    path('', views.index_view, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include(router.urls)),
]
