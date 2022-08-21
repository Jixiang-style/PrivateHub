from django.conf import settings
from urllib.parse import urlencode,parse_qs
from urllib.request import  urlopen
import logging,json

logger = logging.getLogger("django")

class OAuthQQTokenError(Exception):
    pass

class OAuthQQErrorOpenID(Exception):
    pass

class OAuthQQErrorUserInfo(Exception):
    pass

class OAuthQQUser(object):
    """QQ第三方登陆工具类"""
    def __init__(self, app_id=None, app_key=None, redirect_uri=None, state=None):
        self.app_id = app_id or settings.QQ_APP_ID
        self.app_key = app_key or settings.QQ_APP_KEY
        self.redirect_url = redirect_uri or settings.QQ_REDIRECT_URL
        self.state = state or settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径

    def get_auth_url(self):
        """提供QQ登录地址"""
        params = {
            'response_type': 'code',
            'client_id': self.app_id,
            'redirect_uri': self.redirect_url,
            'state': self.state,
            'scope': 'get_user_info',
        }

        url = "https://graph.qq.com/oauth2.0/authorize?" + urlencode(params)

        return url

    def get_access_token(self,code):
        """获取access token"""
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.app_id,
            'client_secret': self.app_key,
            'redirect_uri': self.redirect_url,
            'code': code,
        }

        # urlencode 把字典转换成查询字符串的格式
        url = 'https://graph.qq.com/oauth2.0/token?' + urlencode(params)

        try:
            response = urlopen(url)
            response_data = response.read().decode()
            # parse_qs　把查询字符串格式的内容转换成字典[注意：转换后的字典，值是列表格式]
            data = parse_qs(response_data)
            if data.get('access_token') != None:
                access_token = data.get('access_token')[0]
                refresh_token = data.get('refresh_token')[0]
            else:
                raise OAuthQQTokenError("code已经过期了")
        except:
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise OAuthQQTokenError

        return access_token,refresh_token

    def get_open_id(self, access_token):
        """获取用户的openID"""
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            data = json.loads(response_data[10:-4])
            openid = data.get('openid')
        except:
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise OAuthQQErrorOpenID

        return openid

    def get_user_info(self,access_token,openid):
        """获取QQ用户的信息"""
        params = {
            'access_token': access_token,
            'oauth_consumer_key': self.app_id,
            'openid': openid,
        }

        url = 'https://graph.qq.com/user/get_user_info?' + urlencode(params)
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            data = json.loads(response_data)
            return data
        except:
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise OAuthQQErrorUserInfo