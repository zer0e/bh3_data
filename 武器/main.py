import requests,re,os,time,sys,copy,json

host = "localhost"
username = "root"
password = "soft"
database = "bh3"
table = "weapon"
if_download_image = False
if_use_sql = False

if if_use_sql:
    import pymysql
    db = pymysql.connect(host, username, password, database)
base_url = "http://3rdguide.com"
weapon_url = "http://3rdguide.com/web/arm/index?page={0}&type={1}"
image_dir = './image/'
headers = {
    'X-Requested-With':'XMLHttpRequest'
}
weapon = {
    'weapon_name':'','weapon_img':'','weapon_intro':'','weapon_class':'','weapon_star':'',
    'weapon_attack':'','weapon_huixin':'','skill1':'','skill2':'','skill3':'',
}
weapons = []

def get_weapon_image(image_url):
    if not if_download_image:
        return
    r = requests.get(image_url,headers=headers)
    date_dir = image_dir + image_url[-22:-15]
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    with open(image_dir + image_url[-22:],'wb') as f:
        f.write(r.content)

def get_weapon_by_type(type_id):
    weapon_url_1 = weapon_url.format(1,type_id)
    r = requests.get(weapon_url_1,headers=headers)
    totalPage = r.json()['totalPage']
    for i in range(1,totalPage+1):
        weapon_url_1 = weapon_url.format(i,type_id)
        r = requests.get(weapon_url_1,headers=headers)
        data = r.json()['data']
        format_weapon_data(data,type_id)


def format_weapon_data(data,type_id):
    for i in data:
        weapon_name = i['armsName']
        weapon_class = type_id
        weapon_star = i['weapon_star']
        weapon_intro = i['weapon_intro']
        weapon_attack = i['armsgj']
        weapon_huixin = i['armshx']
        weapon_img = "http:" + i['armsImg']
        detail_url = base_url + i['armsurl']
        skill1 = ''
        skill2 = ''
        skill3 = ''
        # 下载图片
        get_weapon_image(weapon_img)
        # 进入详情页
        r1 = requests.get(detail_url)
        skill = re.findall("height=\"68\">\n([\s\S]*?)</p>",r1.text)
        tmp = []
        for s in skill:
            tmp.append(s.strip().replace("\r\n",""))
        
        skill = tmp
        # print(weapon_name)
        # print(tmp)
        skill_num = len(skill)
        if skill_num == 1:
            skill1 = skill[0]
        elif skill_num == 2:
            skill1 = skill[0]
            skill2 = skill[1]
        elif skill_num == 3:
            skill1 = skill[0]
            skill2 = skill[1]
            skill3 = skill[2]
        
        new_weapon = copy.deepcopy(weapon)
        new_weapon['weapon_name'] = weapon_name
        new_weapon['weapon_class'] = weapon_class
        new_weapon['weapon_star'] = weapon_star
        new_weapon['weapon_intro'] = weapon_intro
        new_weapon['weapon_attack'] = weapon_attack
        new_weapon['weapon_huixin'] = weapon_huixin
        new_weapon['weapon_img'] = weapon_img
        new_weapon['skill1'] = skill1
        new_weapon['skill2'] = skill2
        new_weapon['skill3'] = skill3
        print(new_weapon)
        weapons.append(new_weapon)
        insert_data(new_weapon)
        # time.sleep(2)
        # get_weapon_image("http:"+i['armsImg'])


def insert_data(weapon):
    if not if_use_sql:
        return 
    global db
    cursor = db.cursor()
    keys = ",".join(weapon.keys())
    values = ",".join(['%s'] * len(weapon))
    sql = """insert into {table}({keys})
            values ({values})""".format(table=table, keys=keys, values=values)
    try:
        cursor.execute(sql, tuple(weapon.values()))
        db.commit()
    except:
        db.rollback()


def main():
    for i in range(1,8):
        get_weapon_by_type(i)
    with open("weapon.json",'w',encoding="UTF-8") as f:
        f.write(json.dumps(weapons,ensure_ascii=False))


if __name__ == "__main__":
    main()
