from django.conf.urls import url

from . import views

urlpatterns =[
    url(r'^imagecodes/(?P<image_code_id>.+)/$',views.RegisterImageCodeAPIView.as_view()),
    url(r'^smscodes/(?P<mobile>1[3456789]\d{9})/$',views.RegisterSmsCodeAPIView.as_view()),
]