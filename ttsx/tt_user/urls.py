from django.conf.urls import url
import views

urlpatterns = [
    url("^register$",views.register),
    url("^register_cl$",views.register_cl),
    url("^nameycl/(\w+)$",views.nameycl),
    url("^login$",views.login),
    url("^pwd_cl$",views.pwd_cl),
    url("^cookie/(\w*)",views.cookie),
    url("^centerinfo$",views.centerInfo),
    url("^centersite$",views.centerSite),
    url("^centerorder$",views.centerOrder),
    url("^zhuxiao$",views.zhuxiao),

]