"""
Definition of urls for TangoProject.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

from netchan import views

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^$', views.index.as_view(), name='index'),
        url(r'^netchan/', include('netchan.urls')),
        url(r'^accounts/register/', views.MyRegistrationView.as_view(), name='registration_register'), # turns out urls run in order so custom ones first
        url(r'^accounts/', include('registration.backends.simple.urls')), # sends us to the built in in redux
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
     urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^$', views.index.as_view(), name='index'),
        url(r'^netchan/', include('netchan.urls')),
        url(r'^accounts/register/', views.MyRegistrationView.as_view(), name='registration_register'), # turns out urls run in order so custom ones first
        url(r'^accounts/', include('registration.backends.simple.urls')), # sends us to the built in in redux
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
