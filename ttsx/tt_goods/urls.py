from django.conf.urls import url,include
import views
from views import *

urlpatterns = [
    url("^$",views.index),
    url("^list/(\d)(\d)(\d+)",views.goodslist),
    url("^detail/(\d+)",views.detail),
    url(r'^search/', MySearchViews()),
]