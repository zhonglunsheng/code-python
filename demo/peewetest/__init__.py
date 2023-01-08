# 从数据库表生成model模型，需要安装依赖peewee

# python -m pwiz -e mysql -H 127.0.0.1 -p 3306 -u root -P world -t country >model.py
# -t 指定表名 -P 数据库 执行后需要手动输入密码