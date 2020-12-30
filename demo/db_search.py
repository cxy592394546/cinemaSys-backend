#!/usr/bin/python
import pymysql


def search(datatype, args):
    # 打开数据库连接
    db = pymysql.connect("106.14.220.105", "qingxu", "qingxu", "cinema_db")

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    data_table = []
    if datatype[0] == "cinema":
        # SQL 查询语句
        sql = "SELECT * FROM " + datatype[0]
        try:
            # 执行SQL语句
            cursor.execute(sql)

            # 获取所有记录列表
            results = cursor.fetchall()
            key_id = datatype[0] + 'Id'
            for row in results:
                table = {key_id: row[0], 'info': row[1]}
                data_table.append(table)

            return data_table
        except:
            print("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()

    elif datatype[0] == "room" or datatype[0] == "seat":
        # SQL 查询语句
        sql = "SELECT * FROM " + datatype[0] + " WHERE " + datatype[1] + "Id = %s" % args[0]
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            key_id0 = datatype[0] + 'Id'
            key_id1 = datatype[1] + 'Id'
            for row in results:
                table = {key_id0: row[0], key_id1: row[1], 'info': row[2]}
                data_table.append(table)

            return data_table
        except:
            print("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()

    elif datatype[0] == "session":
        # SQL 查询语句
        sql = "SELECT * FROM " + datatype[0]
        try:
            # 执行SQL语句
            cursor.execute(sql)

            # 获取所有记录列表
            results = cursor.fetchall()
            key_id = datatype[0] + 'Id'
            for row in results:
                table = {key_id: row[0], 'roomId': row[1], 'movieId': row[2], 'time': row[3]}
                data_table.append(table)

            return data_table
        except:
            print("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()

    else:
        print("datatype error")

#
# if __name__ == '__main__':
#     print(search(['cinema'], []))
