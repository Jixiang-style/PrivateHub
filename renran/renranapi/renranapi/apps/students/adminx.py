import xadmin

from .models import Student
class StudentModelAdmin(object):
    list_display = ["id","name","age","my_class_number"]
    list_editable = ["age"] # 允许直接在列表页面中修改的字段
    show_detail_fields = ["name"] # 允许用户通过点击哪些即可查看整个模型里面所有的数据
    refresh_times = [3,30,60,90]            # 设置当前列表页在指定事件内刷新页面
    def my_class_number(self,obj):
        return obj.class_number+"班"

    my_class_number.short_description = "班级"

    data_charts = {
        "student_age_list": {
            'title': '学生年龄分布图',
            "x-field": "age",
            "y-field": ('class_number',),
            "order": ('id',)
        },
        #    支持生成多个不同的图表
       # "order_amount": {
       #   'title': '图书发布日期表',
       #   "x-field": "pub_date",
       #   "y-field": ('title',),
       #   "order": ('id',)
       # },
    }

    model_icon = 'fa fa-film' # https://v3.bootcss.com/components/

xadmin.site.register(Student, StudentModelAdmin)