from rest_framework.views import APIView
from tablestore import PK_AUTO_INCR,TableMeta,TableOptions,ReservedThroughput,CapacityUnit,OTSClient,Row
from django.conf import settings
from rest_framework.response import Response

class TableAPIView(APIView):
    @property
    def ots_client(self):
        """表格存储对象"""
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)
    def post(self,request):
        """创建数据表"""
        # 设置表名
        table_name = "user_message_table"
        # 设置主键列和字段列
        # 主键列
        schema_of_primary_key = [
            ('user_id', 'INTEGER'),
            ('sequence_id', 'INTEGER',PK_AUTO_INCR), # PK_AUTO_INCR 自增
            ("sender_id",'INTEGER'),
            ("message_id",'INTEGER')
        ]

        # 设置表的元信息
        table_meta = TableMeta(table_name, schema_of_primary_key)
        # 设置数据的有效型(表数据的有效期,历史版本)
        table_option = TableOptions(7 * 86400, 5)
        # 设置数据的预留读写吞吐量
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        # 创建表
        self.ots_client.create_table(table_meta, table_option, reserved_throughput)

        return Response({"message": "ok"})

    def delete(self,request):
        """删除表"""
        table = "user_message_table"
        self.ots_client.delete_table(table)
        return Response({"message":"ok"})

    def get(self,request):
        """列出所有的表"""
        table_list = self.ots_client.list_table()
        for table in table_list:
            print(table)

        return Response({"message": "ok"})

from datetime import datetime
from tablestore import BatchWriteRowRequest,TableInBatchWriteRowItem,OTSClientError,PutRowItem,INF_MIN,INF_MAX,CompositeColumnCondition, LogicalOperator, SingleColumnCondition,ComparatorType,Direction,Condition,RowExistenceExpectation
from rest_framework.viewsets import ViewSet
class DataAPIViewSet(ViewSet):
    """操作数据"""
    @property
    def ots_client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)
    def post(self, rquest):
        """添加一条数据"""
        # 指定表名
        table_name = "user_message_table"
        # 主键列[自增主键列的值固定为PK_AUTO_INCR,其他主键列则必须填写具体的值]
        primary_key = [
            # ('主键名', 值),
            ('user_id', 3),  # 接收Feed的用户ID
            ('sequence_id', PK_AUTO_INCR),  # 如果是自增主键，则值就是 PK_AUTO_INCR
            ("sender_id", 1),  # 发布Feed的用户ID
            ("message_id", 4),  # 文章ID
        ]

        # 字段列
        attribute_columns = [
            ('recevice_time', datetime.now().timestamp()),
            ('read_status', False)
        ]

        try:
            row = Row(primary_key, attribute_columns)
            consumed, return_row = self.ots_client.put_row(table_name, row)
        except OTSClientError:
            return Response("添加数据失败!")

        print("consumed--->",consumed)
        print("return_row--->",return_row)
        return Response({"message": "ok"})
    def get(self, request):
        """获取一条数据"""
        # 表名
        table_name = "user_message_table"
        # 必须指定主键
        primary_key = [
            ('user_id', 3),
            ('sequence_id', 1584523834983000),
            ("sender_id",1),
            ("message_id",4)
        ]
        columns_to_get = []
        # return_row 查询结果
        # next_token 最后一条数据的主键ID
        consumed, return_row, next_token = self.ots_client.get_row(table_name, primary_key, columns_to_get)
        print("return_row--->", return_row)

        if return_row:
            print( return_row.primary_key )
            print( return_row.attribute_columns )
        return Response({"message": "ok"})
    def get2(self,request):
        """获取多条数据"""
        table_name = "user_relation_table"
        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', INF_MIN),
            ('follow_user_id', INF_MIN)
        ]

        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', INF_MAX),
            ('follow_user_id',INF_MAX)
        ]


        # 查询所有列
        columns_to_get = []  # 表示返回所有列
        # 结果的数据量
        limit = 10

        consumed, next_start_primary_key, row_list, next_token = self.ots_client.get_range(
            table_name, Direction.FORWARD,
            inclusive_start_primary_key, exclusive_end_primary_key,
            columns_to_get,
            limit=limit,
            max_version=1,
        )
        # 如果使用了多条件查询,则字段查询就会失效,
        # 如果使用了字段查询就不要使用多条件传销
        print("一共返回了：%s" % len(row_list))
        for row in row_list:
            print(row.primary_key, row.attribute_columns)
        return Response({"message": "ok"})

    def post2(self,request):
        """添加多条数据"""
        # 表名
        table_name = "user_message_table"
        # 要添加的数据必须保存到一个列表中
        put_row_items = []

        for i in range(0, 10):
            # 主键列
            primary_key = [  # ('主键名', 值),
                ('user_id', i),  # 接收Feed的用户ID
                ('sequence_id', PK_AUTO_INCR),  # 如果是自增主键，则值就是 PK_AUTO_INCR
                ("sender_id", 1),  # 发布Feed的用户ID
                ("message_id", 5),  # 文章ID
            ]
            attribute_columns = [('recevice_time', datetime.now().timestamp()), ('read_status', False)]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.ots_client.batch_write_row(request)
        print(result)
        print(result.is_all_succeed()) # 判断是否全部数据写入成功!

        return Response({"message":"ok"})