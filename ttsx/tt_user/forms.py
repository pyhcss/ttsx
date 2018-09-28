# coding=utf-8
from django import forms
from captcha.fields import CaptchaField


class Check_Code(forms.Form):
    """生成并验证验证码的类"""
    captcha = CaptchaField()
