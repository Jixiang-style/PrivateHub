from django.core.management import BaseCommand
from django.conf import settings
from tablestore import OTSClient,TableMeta, CapacityUnit, TableOptions, ReservedThroughput,PK_AUTO_INCR
# class Command(BaseCommand):
#     help = """测试命令的帮助文档"""
#     def add_arguments(self, parser):
#         """参数设置"""
#         parser.add_argument("argument", nargs="*", help="必填参数的说明")  # 位置参数
#         parser.add_argument("--option", '-p', default=None, help="可选参数的说明")  # 选项参数
#
#     def handle(self, *args, **options):
#         """命令主方法"""
#         argument = options.get("argument")  # 获取位置参数
#         option = options.get("option")  # 获取位置参数
#         self.stdout.write("argument: %s" % argument)
#         self.stdout.write("option: %s" % option)


class Command(BaseCommand):
    help = """表格存储命令必须接收而且只接收1个命令参数，如下：
        create  表示创建项目使用的表格
        delete  表示删除项目使用的表格
        """
    def add_arguments(self,parser):
        """参数设置"""
        parser.add_argument("argument",nargs="*", help="操作类型") # 位置参数

    def handle(self, *args, **options):
        """表格存储的初始化"""
        argument = options.get("argument")
        if len(argument)==1:
            if argument[0] == "create":
                """创建表格"""
                self.create_table()

            elif argument[0] == "delete":
                """删除表格"""
                self.delete_table()
            else:
                self.stdout.write(self.help)
        else:
            self.stdout.write(self.help)

    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)


    def set_table(self,table_name,schema_of_primary_key,time_to_live=-1):
        # 设置表的元信息
        table_meta = TableMeta(table_name, schema_of_primary_key)
        # 设置数据的有效型
        table_option = TableOptions(time_to_live=time_to_live, max_version=5)
        # 设置数据的预留读写吞吐量
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        # 创建数据
        self.client.create_table(table_meta, table_option, reserved_throughput)


    def create_table(self):
        # 创建存储库
        table_name = "user_message_table"
        schema_of_primary_key = [  # 主键列
            ('user_id', 'INTEGER'),
            ('sequence_id', 'INTEGER', PK_AUTO_INCR),
            ("sender_id", 'INTEGER'),
            ("message_id", 'INTEGER')
        ]

        self.set_table(table_name, schema_of_primary_key, time_to_live=7 * 86400)
        self.stdout.write("创建表格%s完成" % table_name)

        #　关系库
        table_name = "user_relation_table"
        # 主键列
        schema_of_primary_key = [
            ('user_id', 'INTEGER'),
            ("follow_user_id", 'INTEGER'),
        ]
        self.set_table(table_name, schema_of_primary_key)
        self.stdout.write("创建表格%s完成" % table_name)

        # 未读池
        table_name = "user_message_session_table"
        # 主键列
        schema_of_primary_key = [
            ('user_id', 'INTEGER'),
            ("last_sequence_id", 'INTEGER'),
        ]
        self.set_table(table_name, schema_of_primary_key)
        self.stdout.write("创建表格%s完成" % table_name)

    def delete_table(self):
        """删除表"""
        table_list = self.client.list_table()
        for table in table_list:
            self.client.delete_table(table)
            self.stdout.write("删除%s完成" % table)