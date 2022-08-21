from rest_framework.views import APIView
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from django.conf import settings
from rest_framework.response import Response

import logging
loger = logging.getLogger("django")

# Create your views here.
class CaptchaAPIView(APIView):
    """验证码的API接口"""
    def post(self,request):
        AppSecretKey = settings.TENCENT_CAPTCHA.get("App_Secret_Key")
        appid = settings.TENCENT_CAPTCHA.get("APPID")
        Ticket = request.data.get("ticket")
        Randstr = request.data.get("randstr")
        UserIP = request._request.META.get("REMOTE_ADDR")
        params = {
            "aid": appid,
            "AppSecretKey": AppSecretKey,
            "Ticket": Ticket,
            "Randstr": Randstr,
            "UserIP": UserIP
        }
        params = urlencode(params)

        ret = self.txrequest(AppSecretKey, params)
        return Response({"message":ret, "randstr":Randstr})

    def txrequest(self,appkey, params, m="GET"):
        url = "https://ssl.captcha.qq.com/ticket/verify"
        if m == "GET":
            f = urlopen("%s?%s" % (url, params))
        else:
            f = urlopen(url, params)

        content = f.read()
        res = json.loads(content)
        if not res:
            return False
        else:
            error_code = res["response"]
            if error_code == "1":
                return True
            else:
                # 记录日志
                loger.error("验证接口异常!%s:%s" % (res["response"], res["err_msg"]))
                return False

from .utils import get_user_by_data
from rest_framework import status
class CheckMobileAPIView(APIView):
    def get(self,request,mobile):
        user = get_user_by_data(mobile=mobile)
        if user is None:
            return Response({"err_msg":"ok", "err_status":1})
        else:
            return Response({"err_msg":"当前手机号已经被注册","err_status": 0}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import CreateAPIView
from .serializers import UserCreateModelSerializer
from .models import User
class UserAPIView(CreateAPIView):
    """添加用户"""
    queryset = User.objects.all()
    serializer_class = UserCreateModelSerializer

import random
from django_redis import get_redis_connection
from renranapi.settings import constants
import logging
loger = logging.getLogger("django")

class SMSCodeAPIView(APIView):
    """
    短信验证码
    """
    def get(self,request,mobile):
        # 1. 验证数据[短信发送间隔]
        redis = get_redis_connection("sms_code")
        result = redis.get("interval_%s" % mobile)
        if result:
            return Response({"message": "短信已经发送中,请留意您的手机,不要频繁点击!"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 生成随机短信验证码
        sms_code = "%04d" % random.randint(0,9999)

        # 3. 调用异步任务, 发送短信验证码
        from mycelery.sms.tasks import send_sms
        send_sms.delay(mobile=mobile,sms_code=sms_code)

        # 4. 保存短信验证码到redis中
        pipe = redis.pipeline() # 创建管道对象
        pipe.multi() # 开启事务
        # 设置事务中的相关命令
        pipe.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        pipe.setex("interval_%s" % mobile, constants.SMS_INTERVAL_TIME, "_")
        # 提交事务
        pipe.execute()

        # 5. 返回操作结果
        return Response({"message":"短信已经发送,请留意您的手机"})