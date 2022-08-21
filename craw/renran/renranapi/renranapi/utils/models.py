from django.db import models
class BaseModel(models.Model):
    name = models.CharField(null=True, blank=True, max_length=150, verbose_name='标题')
    orders = models.IntegerField(verbose_name='显示顺序')
    is_show=models.BooleanField(verbose_name="是否上架",default=True)
    is_delete=models.BooleanField(verbose_name="逻辑删除",default=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        # 设置当前模型在数据迁移的时候不要为它创建表
        abstract = True

    def __str__(self):
        return self.name
