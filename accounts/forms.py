import re
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from accounts.models import FamoUser

class RegistrationForm(forms.Form):
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            FamoUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    username = forms.CharField(label='ユーザー名（変更不可）', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    password1 = forms.CharField(label='パスワード',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='パスワード（確認用）',
                        widget=forms.PasswordInput())
