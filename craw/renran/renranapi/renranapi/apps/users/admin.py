from django.contrib import admin
# Register your models here.
from .models import User
class UserModelAdmin(admin.ModelAdmin):
    """用户模型管理类"""
    date_hierarchy = 'last_login' # 按时间不同进行展示数据列表
    list_display = ['id', 'nickname',"username","last_login","is_superuser","email","my_mobile"]  # 设置列表页的展示字段
    ordering = ['-last_login'] # 设置默认排序字段,字段前面加上-号表示倒叙排列
    actions_on_bottom = True  # 下方控制栏是否显示,默认False表示隐藏
    actions_on_top = True     # 上方控制栏是否显示,默认False表示隐藏
    list_filter = ["is_superuser"] # 过滤器,按指定字段的不同值来进行展示
    search_fields = ["nickname"] # 搜索内容

    # 自定义字段的值,不能和模型同名
    def my_mobile(self, obj):
        # obj 表示当前模型
        if obj.mobile:
            return obj.mobile[:3]+"* * * *"+obj.mobile[-3:]
        else:
            return None

    my_mobile.empty_value_display = '-暂无-' # 自定义字段空值的时候,填补的默认值
    my_mobile.short_description = "手机号"   # 自定义字段的描述信息
    my_mobile.admin_order_field = "mobile"  # 自定义字段点击时使用哪个字段作为排序条件

    def save_model(self, request, obj, form, change):
        """当站点保存当前模型时"""
        print("有人修改了模型信息[添加/修改]")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """当站点删除当前模型时"""
        super().delete_model(request, obj)

    # 详情页中的展示字段
    # fields = ('nickname', 'username', 'mobile',"avatar") # exclude 作用与fields相反
    readonly_fields = ["nickname"] # 设置只读字段

    # 字段集,fieldsets和fields只能使用其中之一
    fieldsets = (
        ("必填项", {
            'fields': ('nickname', 'username', 'avatar')
        }),
        ('可选项', {
            'classes': ('collapse',),
            'fields': ('mobile', 'alipay'),
        }),
    )

admin.site.register(User, UserModelAdmin)

