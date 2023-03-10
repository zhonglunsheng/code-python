from peewee import *

database = MySQLDatabase('world', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': '123456'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Country(BaseModel):
    capital = IntegerField(column_name='Capital', null=True)
    code = CharField(column_name='Code', constraints=[SQL("DEFAULT ''")], primary_key=True)
    code2 = CharField(column_name='Code2', constraints=[SQL("DEFAULT ''")])
    continent = CharField(column_name='Continent', constraints=[SQL("DEFAULT 'Asia'")])
    gnp = FloatField(column_name='GNP', null=True)
    gnp_old = FloatField(column_name='GNPOld', null=True)
    government_form = CharField(column_name='GovernmentForm', constraints=[SQL("DEFAULT ''")])
    head_of_state = CharField(column_name='HeadOfState', null=True)
    indep_year = IntegerField(column_name='IndepYear', null=True)
    life_expectancy = FloatField(column_name='LifeExpectancy', null=True)
    local_name = CharField(column_name='LocalName', constraints=[SQL("DEFAULT ''")])
    name = CharField(column_name='Name', constraints=[SQL("DEFAULT ''")])
    population = IntegerField(column_name='Population', constraints=[SQL("DEFAULT 0")])
    region = CharField(column_name='Region', constraints=[SQL("DEFAULT ''")])
    surface_area = FloatField(column_name='SurfaceArea', constraints=[SQL("DEFAULT 0.00")])

    class Meta:
        table_name = 'country'
        schema = 'public'

