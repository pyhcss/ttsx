#coding=utf-8
from django import forms
from captcha.fields import CaptchaField


class Check_Code(forms.Form):
    captcha = CaptchaField()
