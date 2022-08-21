from django.shortcuts import render

# Create your views here.
from .models import Reward
from rest_framework.viewsets import ViewSet
from alipay import AliPay
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import random
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django.db import transaction
from article.models import Article

class AliPayAPIViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_alipay(self):
        # 初始化支付对象
        app_private_key_string = open(settings.ALIAPY_CONFIG["app_private_key_path"]).read()
        alipay_public_key_string = open(settings.ALIAPY_CONFIG["alipay_public_key_path"]).read()

        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"]  # 默认False
        )
        return alipay

    def post(self,request):
        """生成支付的链接地址"""
        # 创建打赏记录
        user = request.user
        # 随机流水号
        trade_no = datetime.now().strftime("%Y%m%d%H%M%S") + ("%06d" % user.id) + ("%06d" % random.randint(1, 999999))

        money = request.data.get("money")
        if money < 0:
            return Response("对不起,支付金额不能小于0元", status=status.HTTP_400_BAD_REQUEST)

        reward = Reward.objects.create(
            user=user,
            money=money,
            article_id=request.data.get("article_id"),
            status=0,
            trade_no=trade_no,
            out_trade_no=None,
            reward_type=request.data.get("pay_type"),
            message=request.data.get("content"),
            orders=0,
        )

        if reward.reward_type == 0:
            # 生成支付链接
            alipay = self.get_alipay()
            # 调用接口
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=reward.trade_no,
                total_amount=float(reward.money), # 打赏金额
                subject="打赏文章",
                return_url=settings.ALIAPY_CONFIG["return_url"],
                notify_url=settings.ALIAPY_CONFIG["notify_url"]  # 可选, 不填则使用默认notify url
            )

            url = settings.ALIAPY_CONFIG["gateway_url"] + order_string
        else:
            # 进行其他类型的支付方式
            url = ""

        return Response(url)

    def return_result(self,request):
        """支付宝同步结果处理"""
        data = request.query_params.dict()
        signature = data.pop("sign")
        alipay = self.get_alipay()
        success = alipay.verify(data, signature)
        if success:
            """支付结果处理"""
            # 开启ORM的mysql事务的自动提交,在with语句范围内,所有的SQL会全部被事务控制,要么一起提交,要么一起不提交
            with transaction.atomic():
                # 设置事务的回滚点,用于指定在事务失败时,在哪一部分的SQL语句无效
                save_id = transaction.savepoint()
                try:
                    # 修改打赏记录的状态为已付款
                    reward = Reward.objects.get(
                        trade_no=data.get("out_trade_no"),
                        status=0,
                    )
                    reward.status = 1
                    reward.save()

                    # 增加文章的打赏人数
                    article = Article.objects.get(pk=reward.article.id)
                    article.reward_count += 1
                    article.save()
                    print(article.user.money)
                    print(reward.money)
                    # 给用户资产增加打赏的资金
                    article.user.money= int((article.user.money + reward.money) * 100) / 100
                    article.user.save()

                    # 参考打赏，实现一个资金流水记录[专门显示在钱包位置]

                except Reward.DoesNotExist:
                    transaction.savepoint_rollback(save_id)
                    return Response("当前打赏已经处理完成!请不要重复提交!")
                except:
                    transaction.savepoint_rollback(save_id)
                    return Response({"message": "支付结果处理有误！"})

                return Response({"message":"支付处理成功!"})
        else:
            return Response({"message": "支付失败！"}, status=status.HTTP_400_BAD_REQUEST)


    def notify_result(self,request):
        """支付宝异步结果处理"""
        data = request.data.dict()
        signature = data.pop("sign")
        alipay = self.get_alipay()
        success = alipay.verify(data, signature)
        if success:
            """支付结果处理"""
            # 开启ORM的mysql事务的自动提交,在with语句范围内,所有的SQL会全部被事务控制,要么一起提交,要么一起不提交
            with transaction.atomic():
                # 设置事务的回滚点,用于指定在事务失败时,在哪一部分的SQL语句无效
                save_id = transaction.savepoint()
                try:
                    # 修改打赏记录的状态为已付款
                    reward = Reward.objects.get(
                        trade_no=data.get("out_trade_no"),
                        status=0,
                    )
                    reward.status = 1
                    reward.save()

                    # 增加文章的打赏人数
                    article = Article.objects.get(pk=reward.article.id)
                    article.reward_count += 1
                    article.save()
                    print(article.user.money)
                    print(reward.money)
                    # 给用户资产增加打赏的资金
                    article.user.money= int((article.user.money + reward.money) * 100) / 100
                    article.user.save()

                    # 参考打赏，实现一个资金流水记录[专门显示在钱包位置]

                except Reward.DoesNotExist:
                    transaction.savepoint_rollback(save_id)
                    return Response("当前打赏已经处理完成!请不要重复提交!")
                except:
                    transaction.savepoint_rollback(save_id)
                    return Response({"message": "支付结果处理有误！"})

                return Response({"message":"支付处理成功!"})
        else:
            return Response({"message": "支付失败！"}, status=status.HTTP_400_BAD_REQUEST)