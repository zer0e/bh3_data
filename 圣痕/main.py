import requests, re, time, os, copy

host = "localhost"
username = "root"
password = "soft"
database = "bh3"
stigma_class_table = "stigma_class"
stigma_table = "stigma"
if_download_image = False
if_use_sql = False

if if_use_sql:
    import pymysql

    db = pymysql.connect(host, username, password, database)

base_url = "http://3rdguide.com"
all_stig_url = "http://3rdguide.com/web/stig/index"
one_stig_url = "http://3rdguide.com/web/stig/detail?id="
get_functions = ["蛋池获取", "活动获取", "锻造获取"]
stigma_stars = [5, 4, 3]
get_function = get_functions[0]
stigma_star = stigma_stars[0]
stigmas = []
stigma_classes = []
image_dir = './image/'

stigma = {
    'name': '', 'class_name': '', 'image': '',
    'hp': '', 'attack': '', 'defense': '',
    'critical': '', 'skill': ''
}
stigma_class = {
    'name': '', 'get_function': '', 'introduce': '',
    'image1': '', 'image2': '', 'star': '',
    'skill1': '', 'skill2': ''
}


def get_img(imgs):
    if not if_download_image:
        return
    for img in imgs:
        r = requests.get("http:" + img)
        date_dir = image_dir + img[-22:-15]
        if not os.path.exists(date_dir):
            os.mkdir(date_dir)
        with open(image_dir + img[-22:], 'wb') as f:
            f.write(r.content)


def get_one_stig(data):
    global get_function, stigma_star
    stig_id = data[0]
    stig_class_img1 = "http:" + data[1]
    stig_class_name = data[2]
    stig_url = one_stig_url + stig_id

    # 根据名称切换获取方式和星级
    if stig_class_name == "查理曼":
        stigma_star = stigma_stars[1]
    if stig_class_name == "夏洛特":
        stigma_star = stigma_stars[2]
    if stig_class_name == "渡鸦·月夜":
        get_function = get_functions[1]
        stigma_star = stigma_stars[0]
    if stig_class_name == "符华·诞辰":
        stigma_star = stigma_stars[1]
    if stig_class_name == "马可波罗":
        get_function = get_functions[2]
        stigma_star = stigma_stars[0]
    if stig_class_name == "斯科特":
        stigma_star = stigma_stars[1]

    # 进入详情页
    r = requests.get(stig_url)
    imgs = re.findall("<img src=\"(.*?)\" alt=\"\">", r.text)[1:-1]
    # print(imgs)
    stig_class_img2 = "http:" + imgs[0]
    stig_class_intro = re.findall("<p class=\"mark-item-19\">([\s\S]*?)</p>", r.text)[0]
    # 一个套装有几件圣痕
    stigs = re.findall("<p>(.*?)</p>", r.text)
    # 处理成官方数据("圣痕名(上)")
    for i in range(len(stigs)):
        origin_name = stigs[i].strip()
        new_name = re.sub("-(.*?)位", r"(\1)", origin_name)
        stigs[i] = new_name
    stig_num = len(stigs)
    # 圣痕数据
    all_data = re.findall("<span>(.*?)</span>", r.text)[:-1]
    # 单件圣痕技能
    all_stig_skill = re.findall("<p class=\"mark-item-19 mb30\">([\s\S]*?)</p>", r.text)

    # 清除技能描述前后空格
    tmp = []
    for s in all_stig_skill:
        tmp.append(s.strip())
    all_stig_skill = tmp

    # 套装技能
    stig_class_skill = re.findall("68\">([\s\S]*?)</p>", r.text)
    # 清除技能描述前后空格
    tmp = []
    for s in stig_class_skill:
        tmp.append(s.strip())
    stig_class_skill = tmp

    # 创建新套装
    new_stig_class = copy.deepcopy(stigma_class)
    new_stig_class['name'] = stig_class_name
    new_stig_class['get_function'] = get_function
    new_stig_class['star'] = stigma_star
    new_stig_class['introduce'] = stig_class_intro
    new_stig_class['image1'] = stig_class_img1
    new_stig_class['image2'] = stig_class_img2
    if len(stig_class_skill) == 2:
        new_stig_class['skill1'] = stig_class_skill[0]
        new_stig_class['skill2'] = stig_class_skill[1]
    else:
        new_stig_class['skill1'] = ''
        new_stig_class['skill2'] = ''

    # 写入新套装
    insert_data(new_stig_class, stigma_class_table)
    # print(new_stig_class['stig_class_name'])
    # 处理单件圣痕
    for i in range(stig_num):
        new_stig = copy.deepcopy(stigma)
        stig_name = stigs[i]
        stig_class = stig_class_name
        stig_img = "http:" + imgs[i + 1]
        stig_hp = all_data[i * 4]
        stig_attack = all_data[i * 4 + 1]
        stig_def = all_data[i * 4 + 2]
        stig_critical = all_data[i * 4 + 3]
        stig_skill = all_stig_skill[i]

        new_stig['name'] = stig_name
        new_stig['class_name'] = stig_class
        new_stig['image'] = stig_img
        new_stig['hp'] = stig_hp
        new_stig['attack'] = stig_attack
        new_stig['defense'] = stig_def
        new_stig['critical'] = stig_critical
        new_stig['skill'] = stig_skill
        print(new_stig['name'])
        # 写入新圣痕
        insert_data(new_stig, "stigma")
    print("")
    # 获取所有图片进行下载
    all_imgs = []
    all_imgs.append(data[1])
    for img in imgs:
        all_imgs.append(img)
    tmp = []
    for img in all_imgs:
        if img != "//static.3rdguide.com/image/":
            tmp.append(img)
    all_imgs = tmp
    get_img(all_imgs)
    # print(all_imgs)
    # time.sleep(1)


def insert_data(data, table):
    global stigmas, stigma_classes
    new_data = copy.copy(data)
    if table == "stigma":
        # print(data['stig_name'])
        stigmas.append(new_data)
    elif table == "stigma_class":
        # print(data['stig_class_name'])
        stigma_classes.append(new_data)
        # print(stigma_classes)
        # time.sleep(5)

    if not if_use_sql:
        return
    global db
    cursor = db.cursor()
    keys = ",".join(data.keys())
    values = ",".join(['%s'] * len(data))
    sql = """insert into {table}({keys})
            values ({values})""".format(table=table, keys=keys, values=values)
    try:
        cursor.execute(sql, tuple(data.values()))
        db.commit()
    except:
        db.rollback()


def get_all_stig():
    r = requests.get(all_stig_url)
    a = re.findall("<a href=\"\/web\/stig\/detail\?id=(.*?)\"[\s\S]*?<img src=\"(.*?)\" alt[\s\S]*?<span>(.*?)</span>",
                   r.text)
    for i in a:
        get_one_stig(i)
    # 写入json
    import json
    with open("stigma.json", "w", encoding='UTF-8') as f:
        f.write(json.dumps(stigmas, ensure_ascii=False))
        f.close()
    with open("stigma_class.json", "w", encoding='UTF-8') as f:
        f.write(json.dumps(stigma_classes, ensure_ascii=False))
        f.close()


def main():
    get_all_stig()


if __name__ == "__main__":
    main()
