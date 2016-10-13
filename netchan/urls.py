from django.conf.urls import url
from netchan import views

urlpatterns = [
        url('^$', views.index, name='index'),
        url('^about/', views.about, name='about'),
    ]