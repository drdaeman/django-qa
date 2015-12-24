# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


# Safe User import for Django < 1.5
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

# With the default User model these will be 'auth.User' and 'auth.user'
# so instead of using orm['auth.User'] we can use orm[user_orm_label]
# See http://kevindias.com/writing/django-custom-user-models-south-and-reusable-apps/
user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'qa_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'qa', ['Tag'])

        # Adding model 'UserProfile'
        db.create_table(u'qa_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm[user_orm_label], unique=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'qa', ['UserProfile'])

        # Adding model 'Question'
        db.create_table(u'qa_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('reward', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.UserProfile'])),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'qa', ['Question'])

        # Adding M2M table for field tags on 'Question'
        m2m_table_name = db.shorten_name(u'qa_question_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'qa.question'], null=False)),
            ('tag', models.ForeignKey(orm[u'qa.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'tag_id'])

        # Adding model 'Answer'
        db.create_table(u'qa_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.Question'])),
            ('answer_text', self.gf('django_markdown.models.MarkdownField')()),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('user_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.UserProfile'])),
        ))
        db.send_create_signal(u'qa', ['Answer'])

        # Adding model 'Voter'
        db.create_table(u'qa_voter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.UserProfile'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.Answer'])),
        ))
        db.send_create_signal(u'qa', ['Voter'])

        # Adding model 'QVoter'
        db.create_table(u'qa_qvoter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.UserProfile'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.Question'])),
        ))
        db.send_create_signal(u'qa', ['QVoter'])

        # Adding model 'Comment'
        db.create_table(u'qa_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.Answer'])),
            ('comment_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('user_data', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qa.UserProfile'])),
        ))
        db.send_create_signal(u'qa', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'qa_tag')

        # Deleting model 'UserProfile'
        db.delete_table(u'qa_userprofile')

        # Deleting model 'Question'
        db.delete_table(u'qa_question')

        # Removing M2M table for field tags on 'Question'
        db.delete_table(db.shorten_name(u'qa_question_tags'))

        # Deleting model 'Answer'
        db.delete_table(u'qa_answer')

        # Deleting model 'Voter'
        db.delete_table(u'qa_voter')

        # Deleting model 'QVoter'
        db.delete_table(u'qa_qvoter')

        # Deleting model 'Comment'
        db.delete_table(u'qa_comment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        user_model_label: {
            'Meta': {
                'object_name': User.__name__,
                'db_table': "'%s'" % User._meta.db_table
            },
            # The only assumption left is that the pk is an AutoField (see below)
            User._meta.pk.attname: ('django.db.models.fields.AutoField', [],
                {'primary_key': 'True',
                'db_column': "'%s'" % User._meta.pk.column}
            ),
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'qa.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_text': ('django_markdown.models.MarkdownField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Question']"}),
            'user_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.UserProfile']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'qa.comment': {
            'Meta': {'object_name': 'Comment'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Answer']"}),
            'comment_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.UserProfile']"})
        },
        u'qa.question': {
            'Meta': {'object_name': 'Question'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'reward': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['qa.Tag']", 'symmetrical': 'False'}),
            'user_data': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.UserProfile']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'qa.qvoter': {
            'Meta': {'object_name': 'QVoter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.UserProfile']"})
        },
        u'qa.tag': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'qa.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['%s']" % user_orm_label, 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'qa.voter': {
            'Meta': {'object_name': 'Voter'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.UserProfile']"})
        }
    }

    complete_apps = ['qa']