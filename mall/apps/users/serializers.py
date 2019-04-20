import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

# from mall import settings
from mall import settings
from users.models import User
from django.core.mail import send_mail


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True, label='确认密码')
    sms_code = serializers.CharField(max_length=6, min_length=6, write_only=True, required=True, label='短信验证码')
    allow = serializers.CharField(required=True, write_only=True, label='是否同意协议')

    token = serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=['username','mobile','password','allow','token','password2','sms_code']
        extra_kwargs={
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):

            # 校验手机号
        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号不满足规则')

        return value

    def validate_allow(self, value):

        if value != 'true':
            raise serializers.ValidationError('您未同意协议')

        return value

        # 多个字段校验 密码和确认密码,短信验证码
        # def validate(self, data):
    def validate(self, attrs):

            # 1.密码和确认密码
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('密码不一致')

        # 2.短信验证码
        # 2.1 用户提交的短信
        sms_code = attrs.get('sms_code')
        # 2.2 获取redis的短信
        # ① 连接redis
        redis_conn = get_redis_connection('code')
        # ② 获取数据
        mobile = attrs.get('mobile')
        redis_code = redis_conn.get('sms_%s' % mobile)
        # ③ 判断数据是否存在(有有效期)
        if redis_code is None:
            raise serializers.ValidationError('短信验证码已过期')
        # 2.3 比对
        if redis_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码输入错误')

        return attrs

    def create(self,validated_data):
        del validated_data['sms_code']
        del validated_data['allow']
        del validated_data['password2']

        user = User.objects.create(**validated_data)

        # return user
        user.set_password(validated_data['password'])
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user

class UserDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model=User
        fields=('id', 'username', 'mobile', 'email', 'email_active')




#更新邮箱
class UserEmailSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields=('email','id')

        extra_kwargs={
            'email':{
                'required':True
            }
        }
    def get_token(self,instance,email):
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
        data = {
            'id': instance.id,
            'email': email
        }
        token = s.dumps(data)
        return token


    def update(self, instance, validated_data):
        email = validated_data.get('email')
        instance.email=email
        instance.save()


        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        s=Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)
        data={
            'id':instance.id,
            'email':email
        }
        token=s.dumps(data)

        token = self.get_token(instance,email)


        subject = '美多商场激活邮件'
        # message,          内容
        message = ''
        # from_email,       谁发送的
        # 谁发送的
        from_email = 'qi_rui_hua@163.com'
        # recipient_list    收件人列表
        recipient_list=['836903920@qq.com']
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=%s' % token.decode()
        html_message='<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
        # from celery_tasks.email.tasks import send_ative_email
        # send_ative_email.delay(instance,email)


        return instance
###############################增删改查

from users.models import Address
class AddressSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')

    class Meta:
        model=Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
        return super().create(validated_data)
