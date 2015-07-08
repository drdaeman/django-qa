from __future__ import absolute_import
from django.conf.urls import patterns, url


urlpatterns = patterns('qa.views',
    url(r'^$', 'index', name='index'),
    url(r'^q/(?P<question_id>\d+)/$', 'detail', name='detail'),
    url(r'^answer/(?P<question_id>\d+)/$', 'answer', name='answer'),
    url(r'^add/$', 'add', name='add'),
    url(r'^answer/$', 'add_answer', name='add_answer'),
    url(r'^vote/(?P<answer_id>\d+)/(?P<question_id>\d+)/$', 'vote', name='vote'),
    url(r'^comment/(?P<answer_id>\d+)/$', 'comment', name='comment'),
    url(r'^search/$', 'search', name='search'),
    url(r'^tag/(?P<slug>\w+)/$', 'tag', name='tag'),
    url(r'^thumb/(?P<question_id>\d+)/$', 'thumb', name='thumb'),

    url(r'^profile/(?P<user_id>\d+)/$', 'profile', name='profile'),
)
