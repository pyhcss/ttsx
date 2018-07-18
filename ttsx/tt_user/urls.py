from django.conf.urls import url
import views

urlpatterns = [
    url("^register$",views.register),
    url("^nameycl/(\w+)$",views.nameycl),
    url("^login$",views.login),
    url("^pwd_cl$",views.pwd_cl),
    url("^cookie/(\w*)",views.cookie),
    url("^centerinfo$",views.centerInfo),
    url("^centersite$",views.centerSite),
    url("^centerorder/?(\d*)$",views.centerOrder),
    url("^zhuxiao$",views.zhuxiao),

]