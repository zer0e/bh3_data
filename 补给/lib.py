import pymysql,json,time,copy

host = "localhost"
username = "root"
password = "soft"
database = "bh3"
table = "gacha_record"


def insert_data(db,data):
    new_data = copy.copy(data)
    # new_data['create_time'] = int(time.time())
    cursor = db.cursor()
    keys = ",".join(new_data.keys())
    values = ",".join(['%s'] * len(new_data))
    sql = """insert into {table}({keys})
            values ({values})""".format(table=table, keys=keys, values=values)
    try:
        cursor.execute(sql, tuple(new_data.values()))
    except:
        db.rollback()

def get_data_from_sql_by_name(name,gacha_time):
    db = pymysql.connect(host,username,password,database)
    cursor = db.cursor(pymysql.cursors.DictCursor)

    if not gacha_time:
        sql = "select uid,name,type,item from {} where name = \"{}\"".format(table,name)
    else:
        sql = """select uid,name,type,item,create_time from {} \
        where name = \"{}\" and create_time > \"{}\" and create_time < \"{}\"
        """.format(table,name,gacha_time[0],gacha_time[1])
    cursor.execute(sql)
    row = cursor.fetchall()
    db.close()
    return row

def get_data_from_sql_by_uid_and_item(db,uid,item):
    # db = pymysql.connect(host,username,password,database)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """select uid,name,type,item,create_time from {} where uid = \"{}\" \
            and item = \"{}\" order by create_time desc limit 1""".format(table,uid,item)
    cursor.execute(sql)
    row = cursor.fetchall()
    if len(row) == 0:
        return None
    return row[0]

def delete_data():
    db = pymysql.connect(host,username,password,database)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """delete from {}""".format(table)
    try:
        cursor.execute(sql)
        db.commit()
        return 1
    except:
        db.rollback()
    return 0
    