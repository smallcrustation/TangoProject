from django.conf.urls import url

from netchan import views, views_ajax


urlpatterns = [
        url(r'^$', views.index.as_view(), name='index'),
        url(r'^about/', views.about.as_view(), name='about'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
        url(r'^add_category/$', views.add_category.as_view(), name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),      
        url(r'^restricted/$', views.restricted, name='restricted'), # LOGIN_URL='' in settings.py   
        url(r'^goto/$', views.track_url, name='goto'),
        url(r'^create/$', views.register_profile, name='register_profile'),
        url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
        url(r'^profile list/$', views.profile_list, name='profile_list'),
        url(r'^like/$', views_ajax.like_category, name='like_category'),
        url(r'^suggest/$', views_ajax.suggest_category, name='suggest_category'),
        url(r'^auto_add_page/$', views_ajax.auto_add_page, name='auto_add_page'),
        url(r'^category_list/$', views.show_cats, name='show_cats'),

        ####### Decomissioned ###
        ### function based view urls
        # url(r'^about/', views.about, name='about'),
        # url(r'^$', views.index, name='index'),
        # url(r'^add_category/$', views.add_category, name='add_category'),

        ### others
        #url(r'^register/$', views.register, name='register'),
        #url(r'^login/$', views.user_login, name='login'),
        #url(r'^logout/$', views.user_logout, name='logout'),
        # url(r'^search/$', views.search, name='search'),  
    ]