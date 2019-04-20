from rest_framework import serializers
from goods.models import SKU

class SKUSerializer(serializers.ModelSerializer):



    class Meta:
        model=SKU
        #        id   name   价格     默认图片               评论量
        fields= ('id', 'name', 'price', 'default_image_url', 'comments')


