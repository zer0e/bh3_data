import requests,json,os,time,hashlib,pymysql,sys,argparse
from lib import insert_data,get_data_from_sql_by_name,get_data_from_sql_by_uid_and_item,delete_data
from lib import host,username,password,database

base_url = "https://api-takumi.mihoyo.com/event/bh3_gacha_show/get"


def get_md5(str1):
    h = hashlib.md5()
    h.update(str1.encode(encoding='utf-8'))
    return h.hexdigest()

def get_json_data():
    h = requests.get(base_url)
    json_data = h.json()
    return json_data

def get_gacha_list():
    json_data = get_json_data()
    gacha_list = json_data['data']['gacha_list']
    return gacha_list

def get_sample_gacha_list():
    json_data = get_json_data()
    gacha_list = json_data['data']['gacha_list']
    new_list = []
    for i in gacha_list:
        new_dict = {'name':i['name'],'valid_time':i['valid_time']}
        new_list.append(new_dict)
    return new_list

'''
name 为 '精准A'，'扩充'，'精准B'
'''
def get_gacha_time_by_name(name):
    sample_list = get_sample_gacha_list()
    valid_time = ''
    for i in sample_list:
        if i['name'] == name:
            valid_time = i['valid_time']
            break
    if not valid_time:
        return ""
    valid_time = valid_time.split("~")
    start = valid_time[0].strip()
    end = valid_time[1].strip()
    start_time = int(time.mktime(time.strptime(start,"%Y-%m-%d %H:%M:%S")))
    end_time = int(time.mktime(time.strptime(end,"%Y-%m-%d %H:%M:%S")))
    return [start_time,end_time]

def get_gacha_record():
    json_data = get_json_data()
    gacha_record = json_data['data']['gacha_record']
    return gacha_record

def get_gacha_record_hash(gacha_record):
    # gacha_record = get_gacha_record()
    record_hash = get_md5(json.dumps(gacha_record))
    return record_hash

def get_sample_gacha_record():
    new_list = []
    gacha_record = get_gacha_record()
    # 加入时间戳
    create_time = int(time.time())
    for i in gacha_record:
        new_dict = {'uid':i['uid'],'name':i['name'],'type':i['type'],'item':i['item'],'create_time':create_time}
        new_list.append(new_dict)
    return new_list


'''
name 为 '其他'，'精准A'，'扩充'，'精准B'
'''
def get_sample_gacha_record_by_name(name='扩充'):
    if name == "扩充":
        name = "扩充补给"
    elif name == '精准A':
        name = "精准A补给"
    elif name == '精准B':
        name = "精准补给B"
    new_list = []
    gacha_record = get_gacha_record()
    for i in gacha_record:
        if i['name'] == name:
            new_dict = {'uid':i['uid'],'name':i['name'],'type':i['type'],'item':i['item']}
            new_list.append(new_dict)
    return new_list

def get_sample_gacha_record_from_sql_by_name(name='扩充',gacha_time=[]):
    if name == "扩充":
        name = "扩充补给"
    elif name == '精准A':
        name = "精准A补给"
    elif name == '精准B':
        name = "精准补给B"
    new_list = []
    gacha_record = get_data_from_sql_by_name(name,gacha_time)
    for i in gacha_record:
        if i['name'] == name:
            new_dict = {'uid':i['uid'],'name':i['name'],'type':i['type'],'item':i['item']}
            new_list.append(new_dict)
    return new_list


'''
name 为 '标配'，'装备'，'精准A'，'精准B'，'扩充'
'''
def get_probability_by_name(name='扩充'):
    gacha_list = get_gacha_list()
    for i in gacha_list:
        if i['name'] == name:
            return i['detail_info']

'''
获取稀有物品，即可以显示在补给中的数据
'''
def get_gacha_rare_items(name='扩充'):
    probability = get_probability_by_name(name)
    if name == '扩充':
        new_list = []
        for i in probability:
            if i['type'] == '角色卡':
                new_list.append(i['name'])
        return new_list
    elif "精准" in name:
        new_list = []
        for i in probability:
            if i['level'] == "4星" and ("武器" in i['type'] or "圣痕" in i['type']):
                new_list.append(i['name'])
        return new_list
    else:
        raise KeyError



def statistical_data_from_sql(name='扩充'):
    analysis_keyword = ['精准A','精准B','扩充']
    if name not in analysis_keyword:
        return "可分析以下补给情况:{}".format(" ".join(analysis_keyword))
    print("正在分析{}补给".format(name))
    # 获取时间与物品
    gacha_time = get_gacha_time_by_name(name)
    items = get_gacha_rare_items(name)
    new_dict = {'number':0}
    data = {}
    for i in items:
        data[i] = 0
    gacha_record = get_sample_gacha_record_from_sql_by_name(name,gacha_time)
    if not gacha_record:
        print("没有数据，请先爬取")
        return new_dict
    for i in gacha_record:
        # 特别处理精准B
        if name == "精准B":
            name = "精准补给B"
        if (name in i['name']) and i['item'] in items:
            new_dict['number'] += 1
            data[i['item']] += 1
    new_dict['data'] = data
    print(new_dict)
    return new_dict

# 饼图分析
# gacha_record 为 list
def get_pie(name,gacha_record):
    try:
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif']=['SimHei']
    except:
        print("不支持饼图分析")
        return
    if gacha_record['number'] == 0:
        print("数据为空不支持饼图分析")
        return
    data = gacha_record['data']
    # 清除为0的数据
    for i in list(data.keys()):
        if data[i] == 0:
            del data[i]
    labels = data.keys()
    values = data.values()
    plt.pie(values,labels=labels,autopct='%1.2f%%')
    plt.title(name)
    plt.show() 


def is_valid_data(db,data):
    uid = data['uid']
    item = data['item']
    now = int(time.time())
    sql_data = get_data_from_sql_by_uid_and_item(db,uid,item)
    if not sql_data:
        return True
    create_time = sql_data['create_time']
    if (now - create_time) > (5*60):
        return True
    else:
        return False

def get_gacha_record_to_sql(num=5):
    db = pymysql.connect(host,username,password,database)
    hash_list = []
    print("一共进行{}次爬取".format(str(num)))
    for i in range(num):
        valid_times = 0
        time1 = time.time()
        print("正在进行第{}次爬取..".format(str(i+1)))
        sample_gacha_record = get_sample_gacha_record()
        record_hash = get_md5(json.dumps(sample_gacha_record))
        if record_hash in hash_list:
            continue
        else:
            hash_list.append(record_hash)
            # 应判断item是否已经存在于数据库中，如何判断是否同一次出货？
            for item in sample_gacha_record:
                # print(item['uid'])
                if is_valid_data(db,item):
                    valid_times += 1
                    insert_data(db,item)
            db.commit()
        print("第{}次爬取成功,本次共爬取有效数据{}条,用时{}秒".format(str(i+1),str(valid_times),str((time.time()-time1))))
        next_time = int(60 * ((-valid_times/40)+5))
        print("下次爬取时间为{}秒后".format(next_time))
        time.sleep(next_time)

def delete_gacha_record():
    if delete_data():
        print("删除数据成功")
    else:
        print("删除数据失败")



def main(args):
    if args.func.__name__ == "get_gacha_record_to_sql":
        args.func(args.times)
    elif args.func.__name__ == "statistical_data_from_sql":
        data = args.func(args.name)
        if args.p:
            get_pie(args.name + "补给",data)
    elif args.func.__name__ == "delete_gacha_record":
        args.func()
    else:
        print("参数不正确")


if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="")
    
    subparsers = parser.add_subparsers(help='')
    parser_a = subparsers.add_parser('get', help='get gacha record')
    parser_a.add_argument('--times','-t', type=int, help='get times',default=5)
    parser_a.set_defaults(func=get_gacha_record_to_sql)

    parser_b = subparsers.add_parser('analysis', help='analysis gacha record')
    parser_b.add_argument('--name','-n', type=str, help='name is \'扩充\' or \'精准A\' or \'精准B\'',default="扩充")
    parser_b.add_argument('-p',action='store_true',default=False)
    parser_b.set_defaults(func=statistical_data_from_sql)

    parser_c = subparsers.add_parser('delete', help='delete gacha record')
    parser_c.set_defaults(func=delete_gacha_record)

    args = parser.parse_args()
    main(args)

