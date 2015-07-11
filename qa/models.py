from __future__ import absolute_import
from django.conf import settings
from django.db import models
from django_markdown.models import MarkdownField


class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('slug',)


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    points = models.IntegerField(default=0)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='qa/static/profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Question(models.Model):
    question_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    tags = models.ManyToManyField(Tag)
    reward = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user_data = models.ForeignKey(UserProfile)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = MarkdownField()
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    user_data = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.answer_text


class Voter(models.Model):
    user = models.ForeignKey(UserProfile)
    answer = models.ForeignKey(Answer)
    vote = models.BooleanField(blank=True)

    class Meta:
        unique_together = (("user", "answer"),)


class QVoter(models.Model):
    user = models.ForeignKey(UserProfile)
    question = models.ForeignKey(Question)
    vote = models.BooleanField(blank=True)

    class Meta:
        unique_together = (("user", "question"),)


class Comment(models.Model):
    answer = models.ForeignKey(Answer)
    comment_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user_data = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.comment_text
