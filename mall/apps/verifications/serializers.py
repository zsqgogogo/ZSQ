from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.response import Response


class RegisterSmsCodeSerializer(serializers.Serializer):
    text=serializers.CharField(max_length=4,min_length=4,required=True,label='图片验证码')
    image_code_id=serializers.UUIDField(label='uuid')


    # 自定义校验多个字段
    def validate(self, attrs):
        text=attrs.get('text')
        image_code_id=attrs.get('image_code_id')
        redis_conn=get_redis_connection('code')

        redis_text=redis_conn.get('image_%s'%image_code_id)

        if redis_text is None:
            raise serializers.ValidationError('图片验证码已过期')
        if text.lower() != redis_text.decode().lower():
            raise serializers.ValidationError('输入不一致')
        return attrs