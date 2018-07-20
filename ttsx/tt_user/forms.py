#coding=utf-8
from django import forms
from captcha.fields import CaptchaField


# 生成并验证验证码的类
class Check_Code(forms.Form):
    captcha = CaptchaField()
