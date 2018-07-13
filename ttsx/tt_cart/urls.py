from django.conf.urls import url
import views

urlpatterns = [
    url(r"^cartinfo$",views.cartInfo),
    url(r"^cartadd/(\d+)/(\d+)/(-?\d+)$",views.cartadd),
    url(r"^revcart/(\d+)/(\d+)/(\d+)$",views.revcart),
]