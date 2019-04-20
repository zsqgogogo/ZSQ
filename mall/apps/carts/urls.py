from django.conf.urls import url
from .views import CartAPIView
urlpatterns=[
    url(r'^$',CartAPIView.as_view())
]