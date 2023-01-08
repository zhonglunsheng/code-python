import asyncio
import time
from typing import List, Iterable

import peewee
import peewee_async
from peewee import *

# 数据库连接池
database = peewee_async.PooledMySQLDatabase('world', user='root', password='123456', host='127.0.0.1',
                                            min_connections=10, max_connections=30)


# 建立模型
class TestModel(Model):
    text = CharField()

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text

    class Meta:
        database = database


# 异步
objects = peewee_async.Manager(database)


async def handler():
    # 创建数据
    await objects.create(TestModel, text='Not bad. Watch this, I am async!')
    # 查询整张表
    all_objects = await objects.execute(TestModel.select())
    for obj in all_objects:
        print(obj.text)


async def handler(func):
    all_objects = await objects.execute(func)
    if not all_objects:
        return
    if not isinstance(all_objects, Iterable):
        print(all_objects)
        return
    for obj in all_objects:
        print(obj.text)



async def execute_sql(sql: str, params: List):
    data = await peewee_async.execute(peewee.RawQuery(sql=sql, params=params, _database=database))
    for obj in data:
        print(obj)
    return data

@database.atomic()
async def execute_with_atomic(func):
    raise Exception()
    all_objects = await objects.execute(func)
    if not all_objects:
        return
    if not isinstance(all_objects, Iterable):
        print(all_objects)
        return
    for obj in all_objects:
        print(obj.text)

async def test():
    # 插入查询
    # await handler()
    # 查询带条件、多个条件、分页、排序
    # await handler(TestModel.select().where(TestModel.text == '1'))
    # 自定义SQL执行
    # await handler(TestModel.raw("select * from testmodel"))
    # await handler(TestModel.select().where(SQL("id = %s limit 1", [1])))
    # data = await execute_sql(sql="select * from testmodel where id = %s", params=[1])


    # 插入
    await objects.execute(TestModel.insert(text = '1'))
    # 批量插入
    # await handler(TestModel.insert_many([{"text": 1}]))

    # 删除
    # await handler(TestModel.delete().where(TestModel.text == '1'))
    # await handler(TestModel.delete().where(SQL("text = %s", [1])))

    # 更新
    # await handler(TestModel.update(text='3').where(TestModel.text == '1'))

    # 事务
    await execute_with_atomic(TestModel.update(text='3').where(TestModel.text == '1'))
    await database.close_async()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()
