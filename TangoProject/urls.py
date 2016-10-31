"""
Definition of urls for TangoProject.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView

from netchan import views

class MyRegistrationView(RegistrationView):
    def get_seccess_url(self, user):
        return '/netchan/'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^netchan/', include('netchan.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')), # sends us to the built in in redux
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
