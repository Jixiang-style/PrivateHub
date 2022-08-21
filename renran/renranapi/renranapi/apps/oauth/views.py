from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OAuthUser
# Create your views here.
from .utils import OAuthQQUser,OAuthQQTokenError,OAuthQQErrorOpenID,OAuthQQErrorUserInfo
class OAuthQQAPIView(APIView):
    def get(self,request):
        """生成QQ登录地址"""
        # 接受来自客户端的状态参数[表示要这个状态信息,希望保留到将来QQ登录成功]
        state = request.query_params.get("state")
        oauth = OAuthQQUser(state=state)
        url = oauth.get_auth_url()
        return Response(url)

from .models import User
from rest_framework import status
class QQUserInfoAPIView(APIView):
    def get(self,request):
        """获取用户信息"""
        # 1. 接受响应回来的code和state
        code = request.query_params.get("code")
        state = request.query_params.get("state")

        if not code:
            return Response("QQ登录异常！请重新尝试登录！")

        try:
            oauth = OAuthQQUser()
            # 2. 使用code获取access_token
            access_token,refresh_token = oauth.get_access_token(code)

            # 3. 使用access_token获取当前QQ用户对应的openID
            openid = oauth.get_open_id(access_token)

        except OAuthQQTokenError:
            return Response({"message":"获取access_token错误!"})
        except OAuthQQErrorOpenID:
            return Response({"message":"获取openid错误!"})
        except OAuthQQErrorUserInfo:
            return Response({"message": "获取用户信息失败!!"})
        except:
            return Response({"message": "网络错误!QQ登陆失败!"})

        # 4. 识别用户是否曾注册过账号
        try:
            qq_user = OAuthUser.objects.get(openid=openid)

            # 修改openid对应用户的access_token以及refresh_token的值
            qq_user.access_token = access_token
            qq_user.refresh_token = refresh_token
            qq_user.save()
            # 如果查找到用户,则表示用户属于有账号非第一次QQ登陆, 直接记录登陆状态
            return self.response_token(qq_user.user)

        except OAuthUser.DoesNotExist:
            # 如果没有查到用户,则表示用户属于第一次QQ登陆,接下来就要前端页面让用户进入账号绑定阶段
            # 使用itsdangerours对openID进行加密
            data = {
                "openid": openid,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            from itsdangerous import TimedJSONWebSignatureSerializer as TJWSerializer
            from django.conf import settings
            ts = TJWSerializer(secret_key=settings.SECRET_KEY, expires_in=300)
            result = ts.dumps(data)
            return Response(result)

    def put(self,request):
        """已有平台账号,属于第一次QQ登陆,账号绑定QQ"""
        # 1. 获取客户端提交的账号信息
        username = request.data.get("username")
        password = request.data.get("password")
        # 解密获取qq用户的相关信息
        qq_user = request.data.get("qq_user")
        from itsdangerous import TimedJSONWebSignatureSerializer as TJWSerializer
        from django.conf import settings
        ts = TJWSerializer(secret_key=settings.SECRET_KEY, expires_in=300)
        data = ts.loads(qq_user)
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        openid = data.get("openid")

        try:
            user = User.objects.get(username=username)
            ret = user.check_password(password)
            if not ret:
                return Response("对不起, 账号或密码错误!", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("对不起,当前账号不存在!", status=status.HTTP_400_BAD_REQUEST)

        # 2. 添加账号和QQ的绑定记录
        try:
            OAuthUser.objects.create(
                name="QQ用户",
                orders=1,
                user=user,
                openid=openid,
                access_token=access_token,
                refresh_token=refresh_token,
            )
        except:
            return Response("QQ和账号绑定失败!请联系客服工作人员!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 3. 返回jwt
        return self.response_token(user)

    def post(self,request):
        """把用户注册的新账号和QQ用户进行绑定"""
        # 1. 接受数据[账号,手机,验证码和密码]
        nickname = request.data.get("nickname")
        mobile = request.data.get("mobile")
        sms_code = request.data.get("sms_code")
        password = request.data.get("password")
        # 解密获取qq用户的相关信息
        qq_user = request.data.get("qq_user")
        from itsdangerous import TimedJSONWebSignatureSerializer as TJWSerializer
        from django.conf import settings
        ts = TJWSerializer(secret_key=settings.SECRET_KEY, expires_in=300)
        data = ts.loads(qq_user)
        access_token = data.get("access_token")
        refresh_token = data.get("access_token")
        openid = data.get("openid")

        # 2. 验证数据
        try:
            User.objects.get(mobile=mobile)
            return Response("手机号已经被注册!", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(nickname=nickname)
            return Response("当前昵称已经被使用!", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        if len(openid) < 1:
            return Response("openID丢失!", status=status.HTTP_400_BAD_REQUEST)

        # todo 2.1 校验sms_code验证码是否正确
        # 3. 添加用户
        try:
            user = User.objects.create_user(
                nickname=nickname,
                username=mobile,
                password=password,
                mobile=mobile,
            )
        except:
            return Response("注册失败!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. 绑定QQ
        try:
            OAuthUser.objects.create(
                name="QQ用户",
                orders=1,
                user=user,
                openid=openid,
                access_token=access_token,
                refresh_token=refresh_token,
            )
        except:
            return Response("QQ和账号绑定失败!请联系客服工作人员!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5. 返回jwt
        return self.response_token(user)

    def response_token(self,user):
        """返回jwt"""
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({
            "token": token,
            'id': user.id,
            'username': user.username,
            'avatar': "" if not user.avatar else user.avatar.url,
            'nickname': user.nickname,
        })