from django.shortcuts import render

# Create your views here.
# 注册
# 请求方式： GET /users/usernames/(?P<username>\w{5,20})/count/
# 检测用户名
# 请求参数：
# 参数 	类型 	说明
# username 	str 	用户名
#
# 返回数据：
#
# json
# 返回值 	类型 	说明
# username 	str 	用户名
# count 	int 	数量

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import User


class RegisterUsernameCountAPIView(APIView):
    def get(self,request,username):
        count=User.objects.filter(username=username).count()
        data={
            'username':username,
            'count':count
        }
        return Response(data)


from .serializers import RegisterUserSerializer, UserDetailSerializer, UserEmailSerializer


class RegisterUserAPIView(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterUserSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)

    # 用户中心
# 请求方式： GET/users/infos/
#
# 返回数据：
# 返回值 	类型 	是否必须 	说明
# id 	int 	是 	用户id
# username 	str 	是 	用户名
# mobile 	str 	是 	手机号
# email 	str 	是 	email邮箱
# email_active 	bool 	是 	邮箱是否通过验证
from rest_framework.permissions import IsAuthenticated

class UserDetail(APIView):
#判断是否登录

    permission_classes = [IsAuthenticated]
    def get(self,request):
        #返回字典数据
        user=request.user
        serializer=UserDetailSerializer(user)
        return Response(serializer.data)



# 保存邮箱
# 请求方式：PUT/users/emails/
#
# 请求参数：
# 参数 	类型 	是否必须 	说明
# email 	str 	是 	Email邮箱
#
# 返回数据：
# 返回值 	类型 	是否必须 	说明
# id 	int 	是 	用户id
# email 	str 	是 	Email邮箱

class UserEmailAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def put(self,request):
        data=request.data

        serializer=UserEmailSerializer(instance=request.user,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # 请求方式：GET / users / emails / verification / ?token=xxx

#验证邮箱激活
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from mall import settings
class UserEmailVerificationAPIView(APIView):
    def get(self,request):

        token= request.query_params.get('token')

        if not token:
            return Response({'message':'缺少token'},status=400)
        s=Serializer(secret_key=settings.SECRET_KEY,expires_in=3600)

        try:
            result=s.loads(token)
        except BadSignature:
            return Response(status=400)

        if not result:
            return Response({'message':'token不正确'},status=400)

        id=result.get('id')
        email=result.get('email')

        try:
            user = User.objects.get(id=id,email=email)
        # user = User.objects.filter().filter()
        except User.DoesNotExist:
            return Response(status=400)

        user.email_active=True
        user.save()
        return Response({'message':'ok'})



        #######################地址增删改查#############################3
        # list
        # GET: / users / addresses /
        # create
        # POST: / users / addresses /
        # destroy
        # DELETE: / users / addresses /
        # action
        # PUT: / users / addresses / pk / status /
        # action
        # PUT: / users / addresses / pk / title /


from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from users.serializers import AddressSerializer


class AddressViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)


    #####增加

    #重写create方法，为了验证地址数据是否大于20个，然后调用父类create重新保存
    def create(self, request, *args, **kwargs):
        count=request.user.addresses.count()
        if count>20:
            return Response({'message':'保存地址数量已经达到上限'},status=400)
        return super().create(request,*args,**kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)