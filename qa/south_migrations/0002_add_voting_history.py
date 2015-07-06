# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'QVoter.vote'
        db.add_column(u'qa_qvoter', 'vote',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding unique constraint on 'QVoter', fields ['user', 'question']
        db.create_unique(u'qa_qvoter', ['user_id', 'question_id'])

        # Adding field 'Voter.vote'
        db.add_column(u'qa_voter', 'vote',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding unique constraint on 'Voter', fields ['user', 'answer']
        db.create_unique(u'qa_voter', ['user_id', 'answer_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Voter', fields ['user', 'answer']
        db.delete_unique(u'qa_voter', ['user_id', 'answer_id'])

        # Removing unique constraint on 'QVoter', fields ['user', 'question']
        db.delete_unique(u'qa_qvoter', ['user_id', 'question_id'])

        # Deleting field 'QVoter.vote'
        db.delete_column(u'qa_qvoter', 'vote')

        # Deleting field 'Voter.vote'
        db.delete_column(u'qa_voter', 'vote')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'Meta': {'unique_together': "(('user', 'question'),)", 'object_name': 'QVoter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.UserProfile']"}),
            'vote': ('django.db.models.fields.BooleanField', [], {})
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'qa.voter': {
            'Meta': {'unique_together': "(('user', 'answer'),)", 'object_name': 'Voter'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qa.UserProfile']"}),
            'vote': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['qa']