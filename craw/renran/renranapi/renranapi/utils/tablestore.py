from tablestore import *
from django.conf import settings
class TableStore(object):
    """tablestore工具类"""
    def __init__(self):
        self.client = OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def get_one(self,table_name, primary_key,columns_to_get = []):
        """根据主键获取一条数据"""
        try:
            consumed, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)
        except:
            return {}
        if return_row is None:
            return {}
        else:
            result = return_row.primary_key + return_row.attribute_columns
            data = {}
            for item in result:
                data[item[0]] = item[1]
            return data

    def add_one(self, table_name, primary_key, attribute_columns):
        """添加一条数据"""
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        try:
            # 调用put_row方法，如果没有指定ReturnType，则return_row为None。
            consumed, return_row = self.client.put_row(table_name, row, condition)
        # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            print(e.get_error_message())
            return False
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            print("put row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (
            e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))
            return False
        return True

    def del_one(self, table_name, primary_key, ):
        """删除一条数据"""
        row = Row(primary_key)
        try:
            consumed, return_row = self.client.delete_row(table_name, row, None)
            # 客户端异常，一般为参数错误或者网络异常。
        except OTSClientError as e:
            print("删除数据失败!, 状态吗:%d, 错误信息:%s" % (e.get_http_status(), e.get_error_message()))
            return False
        # 服务端异常，一般为参数错误或者流控错误。
        except OTSServiceError as e:
            print("update row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (
            e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))
            return False
        return True

    def get_all(self, table_name, inclusive_start_primary_key, exclusive_end_primary_key, limit=None,columns_to_get = None, cond=None):
        """获取多条数据"""
        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            limit,  # 结果数量
            column_filter=cond, # 条件
            max_version=1  # 返回版本数量
        )

        if len(row_list) > 0:
            data = []
            for row in row_list:
                result = row.primary_key + row.attribute_columns
                item_data = {}
                data.append(item_data)
                for item in result:
                    item_data[item[0]] = item[1]
            return data
        else:
            return []

    def do_all(self,table_name,put_row_items=[]):
        """操作多条数据"""
        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)
        return result.is_all_succeed()

    def add_all(self,primary_key,attribute_columns):
        """添加多条数据"""
        row = Row(primary_key, attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE)
        item = PutRowItem(row, condition)
        return item

    def del_all(self,primary_key):
        """删除多条数据"""
        row = Row(primary_key)
        condition = Condition(RowExistenceExpectation.IGNORE)
        item = DeleteRowItem(row, condition)
        return item