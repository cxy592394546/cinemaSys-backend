#!/usr/bin/python
from auto_inc import *

import pymysql


def insert(datatype, args):
    # 打开数据库连接
    db = pymysql.connect("106.14.220.105", "qingxu", "qingxu", "cinema_db")

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    if datatype[0] == "cinema":
        sql = "INSERT INTO " + datatype[0] + "(" + datatype[0] + "ID, " + datatype[0] + "Info)\
            VALUES (%s, '%s')" % (auto_inc(datatype[0]), args[0])

        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("Error: unable insert")

        # 关闭数据库连接
        db.close()

    elif datatype[0] == "room" or datatype[0] == "seat":
        sql = "INSERT INTO " + datatype[0] + "(" + datatype[0] + "ID, " + datatype[1] + "ID," + datatype[0] + "Info)\
            VALUES (%s, %s, '%s')" % (auto_inc(datatype[0]), args[0], args[1])

        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("Error: unable insert")

        # 关闭数据库连接
        db.close()

    elif datatype[0] == "session":
        sql = "INSERT INTO " + datatype[0] + "(" + datatype[0] + "ID, " + datatype[1] + "ID," + datatype[2] + "ID, "\
              + datatype[3] + ")VALUES (%s, %s, %s, '%s')" % (auto_inc(datatype[0]), args[0], args[1], args[2])

        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("Error: unable insert")

        # 关闭数据库连接
        db.close()

    else:
        print("datatype error")

#
# if __name__ == '__main__':
#     insert(['session'], ['ohhhhhh'])
