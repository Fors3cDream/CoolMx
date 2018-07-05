_author_ = "killer"
_date_ = "6/27/18 4:39 PM"

from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile

#登录表单验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


# 验证码form
class RegisterForm(forms.Form):
    user_name = forms.CharField(required=True, min_length=6)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 激活账号
class ActiveForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 忘记密码
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})

# 重置密码
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


