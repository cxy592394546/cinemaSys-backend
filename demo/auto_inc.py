#!/usr/bin/python
import pymysql


def auto_inc(datatype):
    # 打开数据库连接
    db = pymysql.connect(host, username, password, database)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if datatype == "cinema" or datatype == "room" or datatype == "seat" or datatype == "session":
        sql = "SELECT * FROM " + datatype

        try:
            # 执行SQL语句
            cursor.execute(sql)

            # 获取所有记录列表
            results = cursor.fetchall()
            column_id = results[-1][0] + 1

            return column_id
        except:
            print("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()

    else:
        print("datatype error")


# if __name__ == '__main__':
#     i = auto_inc('cinema')
#     print(i)
