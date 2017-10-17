
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    url(r'', include('api.urls', namespace='v1')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)