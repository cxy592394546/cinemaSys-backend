#!/usr/bin/python
import pymysql


def update(datatype, args):
    # 打开数据库连接
    db = pymysql.connect(host, username, password, database)

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    if datatype[0] == "cinema":
        sql = "UPDATE " + datatype[0] + " SET " + datatype[0] + "Info \
            = '%s'" % args[1] + " WHERE " + datatype[0] + "Id = %s" % args[0]
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("Error: unable update")

        # 关闭数据库连接
        db.close()

    elif datatype[0] == "room" or datatype[0] == "seat":
        sql = "UPDATE " + datatype[0] + " SET " + datatype[0] + "Info \
            = '%s'" % args[2] + " WHERE " + datatype[0] + "Id = %s \
            " % args[0] + "AND " + datatype[1] + "Id = %s" % args[1]
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("Error: unable update")

        # 关闭数据库连接
        db.close()

    elif datatype[0] == "session":
        sql = "UPDATE " + datatype[0] + " SET " + datatype[1] + "Id \
            = %s" % args[1] + ", " + datatype[2] + "Id = %s" % args[2]\
              + ", " + datatype[3] + " = '%s'" % args[3]\
              + " WHERE " + datatype[0] + "Id = %s" % args[0]
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("Error: unable update")

        # 关闭数据库连接
        db.close()

    else:
        print("datatype error")
