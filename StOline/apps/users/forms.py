from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):#定义注册界面验证码的FORM
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"}) #定义错误输出字符


class ForgetForm(forms.Form):#定义找回密码验证码的FORM
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"}) #定义错误输出字符

class ModifypwdForm(forms.Form):#定义修改密码界面的FORM
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']