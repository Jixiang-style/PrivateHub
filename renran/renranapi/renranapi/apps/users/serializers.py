from rest_framework import serializers
from .models import User
import re
from .utils import get_user_by_data
from django_redis import get_redis_connection

class UserCreateModelSerializer(serializers.ModelSerializer):
    # 接收字段/ 返回客户端的字段
    sms_code = serializers.CharField(write_only=True, min_length=4, max_length=4, label="短信验证码")
    token = serializers.CharField(read_only=True,label="jwt_token")
    class Meta:
        model = User
        fields = ["nickname","mobile","sms_code","password","username","id","avatar","token"]
        read_only_fields = ["id","username","avatar"]
        extra_kwargs = {
            "mobile":{"write_only":True, },
            "password":{"write_only":True, "min_length": 8,"max_length": 16, },
        }

    def validate(self, attrs):
        # 1. 验证手机格式是否正确
        mobile = attrs.get("mobile")
        if not re.match("^1[3-9]\d{9}$",mobile):
            raise serializers.ValidationError("手机号码格式有误!","mobile")

        # 2. 验证手机是否注册了
        user = get_user_by_data(mobile=mobile)
        if user:
            raise serializers.ValidationError("手机号码已经被注册!", "mobile")

        # 3. 短信是否正确
        redis_conn = get_redis_connection("sms_code")
        redis_sms_code = redis_conn.get("sms_%s" % mobile)
        if redis_sms_code:
            sms_code = attrs.get("sms_code")
            if redis_sms_code.decode() != sms_code:
                raise serializers.ValidationError("验证码错误!")
        else:
            raise serializers.ValidationError("验证码已过期!")

        return attrs

    def create(self, validated_data):
        """保存用户信息"""
        try:
            user = User.objects.create_user(
                username=validated_data.get("mobile"),
                password=validated_data.get("password"),
                nickname=validated_data.get("nickname"),
                mobile=validated_data.get("mobile"),
            )

        except:
            raise serializers.ValidationError("用户注册失败!")

        from rest_framework_jwt.settings import api_settings

        # 首次注册,免登录,手动生成jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        return user