from django.db import models
from renranapi.utils.models import BaseModel
from users.models import User
from article.models import Article

class Reward(BaseModel):
    REWARD_OPT = (
        (0, "支付宝"),
        (1, "余额"),
    )
    STATUS_OPT = (
        (0, "未付款"),
        (1, "已付款"),
        (2, "已取消"),
        (3, "超时取消"),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="打赏用户")
    money = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="打赏金额")
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name="文章")
    status = models.SmallIntegerField(default=0,choices=STATUS_OPT, verbose_name="打赏状态")
    trade_no = models.CharField(max_length=255, null=True, blank=True, verbose_name="流水号")
    out_trade_no = models.CharField(max_length=255, null=True, blank=True, verbose_name="支付平台返回的流水号")
    reward_type = models.SmallIntegerField(default=0,choices=REWARD_OPT, verbose_name="打赏类型")
    message = models.TextField(null=True,blank=True, verbose_name="打赏留言")

    class Meta:
        db_table = "rr_user_reward"
        verbose_name = "打赏记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname+"打赏了"+self.article.user.nickname+"的文章《" +self.article.name+"》"+self.money+"元"