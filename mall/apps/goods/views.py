from django.shortcuts import render

# Create your views here.
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from goods.models import SKU
from .serializers import SKUSerializer

#热销商品GET /goods/categories/(?P<category_id>\d+)/hotskus/
#请求参数category_id


# 返回值 	类型 	是否必须 	说明
# id 	int 	是 	商品sku 编号
# name 	str 	是 	商品名称
# price 	decimal 	是 	单价
# default_image_url 	str 	是 	默认图片
# comments 	int 	是 	评论量

class HotSKUListView(ListCacheResponseMixin,ListAPIView):
    serializer_class = SKUSerializer
    pagination_class =None

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id,is_launched=True).order_by('-sales')[:2]

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5



class SKUListAPIView(ListAPIView):

    serializer_class = SKUSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ['sales', 'price', 'create_time']
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        category_id = self.kwargs['category_id']

        return SKU.objects.filter(category_id=category_id,is_launched=True)