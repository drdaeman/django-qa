from __future__ import absolute_import
from south.modelsinspector import add_introspection_rules


# django-markdown doesn't provide introspection, so we do it here
add_introspection_rules([], ["^django_markdown\.models\.MarkdownField"])
