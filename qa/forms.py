from qa.models import *
from django.contrib.auth.models import User
from django import forms

import django.contrib.auth

auth_user_model = django.contrib.auth.get_user_model()

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fiels = ('question_text', 'tags')
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = auth_user_model
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
