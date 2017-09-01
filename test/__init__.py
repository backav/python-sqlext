#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlext import init_engine, transaction, PROPAGATION, query_all_template, insert_template

db_engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/test?charset=utf8mb4',
                          pool_size=1,
                          max_overflow=1, poolclass=QueuePool, pool_recycle=1200,
                          connect_args={'connect_timeout': 14})

init_engine(db_engine, True)

# query
query = query_all_template("select * from user")
print(str(query()))

# insert with transaction
insert = insert_template("""insert into user (id,name) values (:id,:name)""")


@transaction(propagation=PROPAGATION.REQUIRED)
def insert_two():
    insert(id=2, name='jack')
    if 1 == 1:
        raise Exception('test')

    insert(id=3, name='ben')


insert_two()
