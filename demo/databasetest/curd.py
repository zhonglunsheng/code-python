import json
import re
from typing import List


class Crud:
    def __init__(self, database) -> None:
        self.database = database

    def check_order_by_field(self, value: str):
        pattern = re.compile("[a-zA-Z0-9_ ]+$")
        if re.match(pattern, value):
            return True
        else:
            raise Exception("排序字段非法传入")

    def to_object(self, dict_data, clazz):
        obj = clazz()
        attrs = dir(obj)
        for attr in attrs:
            if attr.startswith('_') or attr.endswith('_'):
                continue
            if hasattr(attr, '__call__'):
                continue
            if attr in dict_data:
                setattr(obj, attr, dict_data.get(attr))

    async def select(self, table_name: str, columns: List = None, condition=None, like_field: List = None,
                     order_field: List = None, page: int = None, size: int = None, convert_dict=False,
                     convert_clazz=None, is_count=True):
        query_sql_prefix = "select "

        if columns and len(columns):
            query_sql_prefix += f" {','.join(columns)} from {table_name}"
        else:
            query_sql_prefix += f" * from {table_name}"

        query_sql = ""
        condition_dict = {}
        if condition:
            query_sql = f"{query_sql} where "
            # SELECT * FROM city WHERE name = :name and
            if not isinstance(condition, dict):
                condition_dict = condition.__dict__
            else:
                condition_dict = condition.copy()

            condition_where_sql = ""
            for k, v in condition_dict.items():
                if like_field and like_field.__contains__(k):
                    # like concat('%', :name, '%')
                    condition_where_sql = "and " + condition_where_sql + f"{k} like concat('%', :{k}, '%')"
                else:
                    condition_where_sql = "and " + condition_where_sql + f"{k} = :{k}"

            # 去掉第一个and
            condition_where_sql = condition_where_sql[3:]
            query_sql += condition_where_sql

        # 处理排序 支持多个
        if order_field and len(order_field):
            query_sql += " order by "
            for item in order_field:
                self.check_order_by_field(item)

            query_sql += ",".join(order_field)

        # 处理分页
        if page and size:
            query_sql += f" limit {(page - 1) * size}, {size}"

        print(query_sql, condition)

        res = await self.database.fetch_all(query_sql_prefix + query_sql, values=condition_dict)

        if convert_dict:
            res = [dict(item) for item in res]

        if convert_clazz:
            dict_list = [json.dumps(dict(item), ensure_ascii=False) for item in res]
            res = [self.to_object(item, convert_clazz) for item in dict_list]

        if is_count:
            query_sql_count_prefix = f"select count(*) as total from {table_name}"
            total = await self.database.fetch_all(query_sql_count_prefix + query_sql, values=condition_dict)
            return res, total
        else:
            return res

    async def select_one(self, table_name: str, columns: List = None, condition=None, like_field: List = None,
                         order_field: List = None, convert_dict=False, convert_clazz=None):
        res = await self.select(table_name=table_name, columns=columns, condition=condition, like_field=like_field,
                                order_field=order_field, convert_dict=convert_dict, convert_clazz=convert_clazz, page=1,
                                size=1)
        return res[0] if res and len(res) else None

    async def execute(self, sql, value):
        return await self.database.execute(sql, values=value)

    async def update(self, *, table_name, data, condition: dict = None):
        if data:
            if not isinstance(data, dict):
                data_dict = data.__dict__
            else:
                data_dict = data.copy()

            # update city set name = :name where name = :name

            sql = f"update {table_name} set "
            set_list = []
            values = {}
            for k, v in data_dict.items():
                set_list.append(f"{k} = :s{k}")
                values['s' + k] = v
            sql += ",".join(set_list)

            if condition:
                sql += " where "
                where_list = []
                for k, v in condition.items():
                    where_list.append(f"{k} = :w{k}")
                    values['w' + k] = v
                sql += " and ".join(where_list)

            return await self.database.execute(sql, values=values)

    async def insert(self, *, table_name, data, prefix="insert into"):
        """
        支持单条或多条插入
        :param table_name:
        :param data:
        :return:
        """
        if data:
            if isinstance(data, list):
                data = [item.__dict__ if not isinstance(item, dict) else item.copy() for item in data]
                data_dict = data[0]
                value = data
            else:
                data_dict = data.__dict__ if not isinstance(data, dict) else data.copy()
                value = data_dict
            # insert into city (name, id) values (:name, :id)
            keys = [ ':' + item for item in data_dict.keys()]
            sql = f"{prefix} {table_name} ({','.join(data_dict.keys())}) values ({','.join(keys)})"

            if isinstance(value, list):
                return await self.database.execute_many(sql, values=value)
            else:
                return await self.database.execute(sql, values=value)

    async def delete(self, *, table_name, condition: dict = None):
        sql = f"delete from {table_name} "
        # delete from city where name = :name
        if condition:
            sql += "where "
            where_list = []
            for k, v in condition.items():
                where_list.append(f"{k} = :{k}")
            sql += " and ".join(where_list)
            return await self.database.execute(sql, values=condition)
