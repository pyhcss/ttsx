from django.conf.urls import url
import views

urlpatterns = [
    url("^register$",views.register),
    url("^register_cl$",views.register_cl),
    url("^login$",views.login),
    url("^login_cl$",views.login_cl),
    url("^centerinfo$",views.centerInfo),
]