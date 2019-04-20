from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializers import ProvienceSerializer,DistrictSerializer

from rest_framework_extensions.cache.decorators import cache_response
#
# class ProvienceAPIView(APIView):
#
#     # @cache_response(timeout=60*60,cache='default')
#     def get(self,request):
#         areas=Area.objects.filter(parent_id=None)
#         serializer=ProvienceSerializer(areas,many=True)
#         return Response(serializer.data)
#
#
# # 返回数据
# # 返回值 	类型 	是否必传 	说明
# # id 	int 	是 	上级区划id（省份id或城市id）
# # name 	str 	是 	上级区划的名称
# # subs 	list[] 	是 	下属所有区划信息
#
# # /areas/infos/(?P<pk>\d+)/
# class DistrictAPIView(APIView):
#     # @cache_response(timeout=60 * 60, cache='default')
#     def get(self,request,pk):
#         areas=Area.objects.filter(parent_id=pk)
#         serializer=DistrictSerializer(areas,many=True)
#         s=serializer.data
#         print(s)
#         return Response(serializer.data)


class ProvienceAPIView(APIView):
    @cache_response(timeout=60 * 60, cache='default')
    def get(self,request):
        area=Area.objects.filter(parent_id=None)
        serializer=ProvienceSerializer(area,many=True)
        return Response(serializer.data)


class DistrictAPIView(APIView):
    # @cache_response(timeout=60 * 60, cache='default')
    def get(self,request,pk):
        area=Area.objects.filter(parent_id=pk)
        serializer=ProvienceSerializer(area,many=True)
        # for i in serializer.data:
        #
        #     return Response(i)
        return Response(serializer.data)
    # [{"id": 110100, "name": "北京市",
    #   "subs": [{"id": 110101, "name": "东城区"}, {"id": 110102, "name": "西城区"}, {"id": 110105, "name": "朝阳区"},
    #            {"id": 110106, "name": "丰台区"}, {"id": 110107, "name": "石景山区"}, {"id": 110108, "name": "海淀区"},
    #            {"id": 110109, "name": "门头沟区"}, {"id": 110111, "name": "房山区"}, {"id": 110112, "name": "通州区"},
    #            {"id": 110113, "name": "顺义区"}, {"id": 110114, "name": "昌平区"}, {"id": 110115, "name": "大兴区"},
    #            {"id": 110116, "name": "怀柔区"}, {"id": 110117, "name": "平谷区"}, {"id": 110118, "name": "密云区"},
    #            {"id": 110119, "name": "延庆区"}]}]

