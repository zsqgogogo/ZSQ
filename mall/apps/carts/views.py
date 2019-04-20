import base64
import pickle

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import request
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.serializers import CartSerializer, CartSKUSerializer
from goods.models import SKU


class CartAPIView(APIView):

    def perform_authentication(self, request):
        pass

    def post(self,request):
        data=request.data
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        sku_id=serializer.validated_data.get('sku_id')
        count=serializer.validated_data.get('count')
        selected=serializer.validated_data.get('selected')

        user=request.user

        if user is not None and user.is_authenticated:
            #redis
            redis_conn = get_redis_connection('cart')
            redis_conn.hset('cart_%s'%user.id,sku_id,count)
            if selected:
                redis_conn.sadd('cart_selected_%s' % user.id, sku_id)

            return Response(serializer.data)
        else:
            cookie_str = request.COOKIES.get('cart')
            if cookie_str is not None:
                bytes_data=base64.b64decode(cookie_str)
                cookie_cart=pickle.loads(bytes_data)

            else:
                cookie_cart={}

            if sku_id in cookie_cart:
                original_count = cookie_cart[sku_id]['count']
                count += original_count

            cookie_cart[sku_id]={
                'count':count,
                'selected':selected
            }

            bytes_dumps=pickle.dumps(cookie_cart)
            bytes_str = base64.encode(bytes_dumps)
            cookie_save_str = bytes_str.decode()
            response= Response(serializer.data)
            response.set_cookie('cart',cookie_save_str,3600)
            return response
            # 一.需求
            # 当用户点击购物车页面的时候, 我们需要让前端将用户信息传递给后端
    # 1. 获取用户信息
    # 2. 判断用户信息
    # 3. 登陆用户从redis中获取数据
    #     3.1 连接redis
    #     3.2 获取redis的数据 hash set  sku_id:count,sku_id:count ,
    #
    # 4. 未登录用户从cookie中获取数据
    #     4.1 从cookie中获取数据
    #     4.2 判断数据是否存在
    #         如果存在则要进行 解码     {sku_id:{count:xxx,selected:xxx}}
    #         如果不存在
    # 5   获取商品的所有的id  [id,id,id]
    # 6   再根据id获取商品的详细信息 [sku,sku,sku,sku]
    # 7   将对象列表转换为字典
            # 8   返回相应
    def get(self,request):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:

            redis_conn = get_redis_connection('cart')
            redis_ids_count = redis_conn.hgetall('cart_%s'%user.id)
            redis_selected_ids = redis_conn.smembers('cart_selected_%s'%user.id)
            cookie_cart = {}
            for id,count in redis_ids_count:

                if id in redis_selected_ids:
                    selected=True
                else:
                    selected=False
                cookie_cart[id]={
                    'count':count,
                    'selected':selected
                }
        else:
            cart_str=request.COOKIES.get('cart')
            if cart_str is not None:
                cookie_cart=pickle.loads(base64.b64decode(cart_str))

            else:
                cookie_cart={}


        ids=cookie_cart.keys()
        skus=SKU.objects.filter(pk__in=ids)

        for sku in skus:
            sku.count=cookie_cart[sku.id]['count']
            sku.selected=cookie_cart[sku.selected]['selected']

        serializer=CartSKUSerializer(skus,many=True)
        return Response(serializer.data)