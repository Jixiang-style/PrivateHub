from mycelery.main import app
from .yuntongxun.sms import CCP
from . import constants
@app.task(name="send_sms")
def send_sms(mobile,sms_code):
    ccp = CCP()
    ret = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME // 60], constants.SMS_TEMPLATE_ID)
    return ret

@app.task()
def sms_notice():
    # 异步任务的代码
    print("短信通知")
    # 任务的返回值
    return "Hello world"