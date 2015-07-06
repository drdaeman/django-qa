from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views


urlpatterns = patterns('',
    url(r'^', include('qa.urls', namespace='qa')),
    url(r'^api/', include('qa.api.urls', namespace='qa-api')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
