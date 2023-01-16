import asyncio

from databases import Database
from curd import Crud

database = Database('mysql+aiomysql://root:123456@localhost:3306/world?min_size=5&max_size=20')

async def test():
    await database.connect()
    # query = "SELECT * FROM city WHERE name = :name"
    # rows = await database.fetch_all(query=query, values={"name": 'Kabul'})

    query = "SELECT * FROM city WHERE name like concat('%', :name, '%')"
    rows = await database.fetch_all(query=query, values={"name": 'abul'})
    print(rows)

    await database.fetch_all(query=query, values={"name": 'abul'})

class City:
    name: str

async def test2():
    await database.connect()
    crud = Crud(database)
    # rows, total = await curd.select(table_name="city", is_count=True)
    # print(rows, total)
    # city = City()
    # city.name = 'k'
    # rows = await curd.select_one(table_name="city", columns=["name"], order_field=["name desc"], condition=city, like_field=['name'], convert_dict=True)
    # print(rows)
    city1 = City()
    city1.name = 'zhonglunsheng333'
    # city = City()
    # city.name = 'zhonglunsheng2'
    # row = await crud.insert(table_name="city", data=[city1, city])
    # print(row)
    #
    # row = await crud.update(table_name="city", data=city1, columns={"name": "zhonglunsheng1"})
    # print(row)

    row = await crud.delete(table_name="city", condition={"name": "zhonglunsheng333"})
    print(row)





if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test2())
    loop.run_forever()
