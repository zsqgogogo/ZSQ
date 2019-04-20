from django.conf.urls import url
from rest_framework import views
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns=[
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountAPIView.as_view()),
    url(r'^$', views.RegisterUserAPIView.as_view()),
    url(r'^auths/$',obtain_jwt_token),
    url(r'^infos/$',views.UserDetail.as_view()),
    url(r'^emails/$',views.UserEmailAPIView.as_view()),
    url(r'^emails/verification/$',views.UserEmailVerificationAPIView.as_view()),
]
from .views import AddressViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'addresses',AddressViewSet,base_name='address')
urlpatterns += router.urls