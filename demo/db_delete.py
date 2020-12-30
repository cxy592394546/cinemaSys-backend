#!/usr/bin/python
import pymysql


def delete(datatype, args):
    # 打开数据库连接
    db = pymysql.connect("106.14.220.105", "qingxu", "qingxu", "cinema_db")

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    if datatype[0] == "cinema" or datatype[0] == "session" or datatype[0] == "seat" or datatype[0] == "room":
        sql = "DELETE FROM " + datatype[0] + " WHERE " + datatype[0] + "Id = %s" % args[0]
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("Error: unable delete")

        # 关闭数据库连接
        db.close()

    else:
        print("datatype error")
