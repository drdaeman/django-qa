from __future__ import absolute_import
from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text', 'tags')
