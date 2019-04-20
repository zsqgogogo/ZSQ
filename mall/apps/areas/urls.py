from django.conf.urls import url
from areas import views


urlpatterns=[
    url(r'^infos/$',views.ProvienceAPIView.as_view()),
    url(r'^infos/(?P<pk>\d+)/$',views.DistrictAPIView.as_view())
]


