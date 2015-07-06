from __future__ import absolute_import
from ..models import Question
from rest_framework import serializers, viewsets
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
