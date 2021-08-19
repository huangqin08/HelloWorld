from captcha.fields import CaptchaField
from django import forms
# from django.forms import From


# class UserForm(From):
from django.forms import Form


class UserLoginForm(Form):
    username = forms.CharField(max_length=20,min_length=8,error_messages={'min_length':'用户名长度至少8位'},label='用户名')
    password = forms.CharField(max_length=16, min_length=6, error_messages={'min_length': '密码长度至少6位','max_length':'密码长度不少于16位'},widget=forms.PasswordInput, label='密码')
    captcha = CaptchaField(label='验证码')
