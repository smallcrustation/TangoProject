"""
Definition of urls for TangoProject.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

from netchan import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^netchan/', include('netchan.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
