from django.conf.urls import url
import views

urlpatterns = [
    url(r"^orderinfo/?(\d*)/?(\d*)$",views.orderInfo),
    url(r"^ordercl/?(\d*)$",views.ordercl),
]
