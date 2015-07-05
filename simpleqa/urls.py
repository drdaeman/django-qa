from django.conf.urls import patterns, include, url
from django.contrib import admin

from qa import views as qa_views
from . import views

from django.conf.urls import url, include
from qa.models import Question
from rest_framework import routers, serializers, viewsets


import django.contrib.auth

auth_user_model = django.contrib.auth.get_user_model()

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = auth_user_model
        fields = ('url', 'username', 'email', 'is_staff')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        model = Question
        fields = ('id', 'pub_date', 'question_text', 'tags', 'views')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = auth_user_model.objects.all()
    serializer_class = UserSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/questions', QuestionViewSet)

urlpatterns = patterns('',
    url(r'^$', qa_views.index, name='index'),
    url(r'^q/(?P<question_id>\d+)/$', qa_views.detail, name='detail'),
    url(r'^answer/(?P<question_id>\d+)/$', qa_views.answer, name='answer'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/$', qa_views.add, name='add'),
    url(r'^answer/$', qa_views.add_answer, name='add_answer'),
    url(r'^vote/(?P<user_id>\d+)/(?P<answer_id>\d+)/(?P<question_id>\d+)/(?P<op_code>\d+)/$',
        qa_views.vote, name='vote'),
    url(r'^comment/(?P<answer_id>\d+)/$', qa_views.comment, name='comment'),
    url(r'^search/$', qa_views.search, name='search'),
    url(r'^tag/(?P<slug>\w+)/$', qa_views.tag, name='tag'),
    url(r'^thumb/(?P<user_id>\d+)/(?P<question_id>\d+)/(?P<op_code>\d+)/$',
        qa_views.thumb, name='thumb'),

    url(r'^profile/(?P<user_id>\d+)/$', qa_views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url('^markdown/', include('django_markdown.urls')),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
