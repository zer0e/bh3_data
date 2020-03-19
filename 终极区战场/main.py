import requests
import random,time,json
import time,sys,re,copy

host = "localhost"
username = "root"
password = "soft"
database = "bh3"
table = "battlefield"
if_use_sql = False
if if_use_sql:
    import pymysql
    db = pymysql.connect(host, username, password, database)

base_url = "http://3rdguide.com"
# 终极区作业地址scene=82
assignments_url= "http://3rdguide.com/web/teamnew/index?jumpfrom=pc&scene=82&strong={0} \
&war=&page={1}&pageSize=50&type=info_score&sort=desc&_=1583036936780"
strongs = {'帕凡提': 97, '影骑士·月轮': 98, '赫菲斯托斯': 99, '地藏御魂': 100, '阿湿波': 101, 'MHT-3和平使者': 102, '空之律者': 103, '姬麟·黑': 104, '贝纳勒斯': 105, '特里波卡': 106, '教父军团': 107, '苍骑士·月魂': 108, '湮灭沉灵': 109, '海姆达尔': 110, '绯狱丸': 112, '卡莲': 113, '吼姆王': 114, '托纳提乌·噬日之影':115}
headers = {
    'Referer':'http://3rdguide.com/web/teamnew/index',
    'X-Requested-With':'XMLHttpRequest'
}

assignment = {'author':'','score':'','scene_name':'','other_name':'',
'team01':'','team01_class':'','team01_equipment':'',
'team02':'','team02_class':'','team02_equipment':'',
'team03':'','team03_class':'','team03_equipment':'',
'figure':'','figure_star':'',
'info_url':'','av':''}

assignments = []

def get_all_strong():
    for i in range(90,120):
        url_1 = assignments_url.format(i,1)
        r = requests.get(url_1,headers=headers)
        if(len(r.json()['data']) != 0):
            print(r.json()['total'])
            strongs[r.json()['data'][0]['info_scene_name']] = i
        else:
            pass

def format_assignment(data):
    global assignments
    for i in range(len(data)):
        new_assignment = copy.deepcopy(assignment)
        info_url = base_url + data[i]['info_url']
        score = data[i]['info_score']
        author = data[i]['info_auth']
        scene_name = data[i]['info_scene_name']
        # 进入详情页
        r1 = requests.get(info_url)
        character_and_equipment = re.findall("<div class=\"mid_item_right_top_data_title\">(.*?)</div>",r1.text)
        character_class = re.findall("<div class=\"rate rate_(.*?)\"></div>",r1.text)
        figure = re.findall("<p>(.*?)</p>",r1.text)[1]
        figure_star = len(re.findall("<i class='star(.*?)'></i>",r1.text))
        try:
            av = re.findall("https?:\/\/(www.bilibili.com\/video\/|b23.tv\/)(.*?)\/?\"\\);",r1.text)[0][1]
        except :
            av = ''

        new_assignment['info_url'] = info_url
        new_assignment['scene_name'] = scene_name
        new_assignment['score'] = score
        new_assignment['author'] = author
        new_assignment['team01'] = character_and_equipment[0]
        new_assignment['team01_class'] = character_class[0]
        new_assignment['team01_equipment'] = ' '.join(character_and_equipment[1:5])
        new_assignment['team02'] = character_and_equipment[5]
        new_assignment['team02_class'] = character_class[1]
        new_assignment['team02_equipment'] = ' '.join(character_and_equipment[6:10])
        new_assignment['team03'] = character_and_equipment[10]
        new_assignment['team03_class'] = character_class[2]
        new_assignment['team03_equipment'] = ' '.join(character_and_equipment[11:])
        new_assignment['figure'] = figure
        new_assignment['figure_star'] = figure_star
        new_assignment['av'] = av
        assignments.append(new_assignment)
        print(new_assignment)
        # insert_data(new_assignment)


def get_assignments_by_id(index_id):
    page_url = assignments_url.format(index_id,1)
    r = requests.get(page_url,headers=headers)
    totalPage = r.json()['totalPage']
    for i in range(1,totalPage+1):
        page_url = assignments_url.format(index_id,i)
        r = requests.get(page_url,headers=headers)
        totalPage = r.json()['totalPage']
        data = r.json()['data']
        format_assignment(data) 
    # 如果数据多于50条则继续
    



def insert_data(assignment):
    if not if_use_sql:
        return 
    global db
    cursor = db.cursor()
    keys = ",".join(assignment.keys())
    values = ",".join(['%s'] * len(assignment))
    sql = """insert into {table}({keys})
            values ({values})""".format(table=table, keys=keys, values=values)
    try:
        cursor.execute(sql, tuple(assignment.values()))
        db.commit()
    except:
        db.rollback()

def get_all_assignments():
    global strongs,assignments
    for key,value in strongs.items():
        assignments = []
        get_assignments_by_id(value)
        with open(key + ".json",'w',encoding='UTF-8') as f:
            f.write(json.dumps(assignments,ensure_ascii=False))
        # print(value)

def main():
    get_all_assignments()

if __name__ == "__main__":
    main()
