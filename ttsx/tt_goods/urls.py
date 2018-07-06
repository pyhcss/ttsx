from django.conf.urls import url
import views

urlpatterns = [
    url("^$",views.index),
    url("^list/(\d)(\d)(\d+)",views.goodslist),
    url("^detail/(\d+)",views.detail),
]