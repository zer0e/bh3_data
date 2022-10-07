import json
import os
import time
import traceback
import pymongo

import requests as r
from bs4 import BeautifulSoup

base_url = "https://api-static.mihoyo.com/common/blackboard/bh3_wiki/v1"

stigma_template = {
    "item_id": "", 'name': '', 'suit_id': None, 'suit_name': '', "icon": "", 'image': '',
    'hp': 0, 'attack': 0, 'defense': 0,
    'critical': 0, 'skill': '', "star": None
}

stigma_suit_template = {
    "suit_id": "", "name": "", "tag": "", "skill1_name": "",
    "skill1_effect": "", "skill2_name": "", "skill2_effect": "",
    'introduction': ''
}
stigma_suit_start_id = 4001
stigma_suit_map = {}
stigma_list = []


def get_stigma_list_from_api():
    stigma_list_url = base_url + "/home/content/list?app_sn=bh3_wiki&channel_id=19"
    req = r.get(stigma_list_url)
    res = req.json()
    with open("stigma_list_req.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))


def get_single_stigma_from_api(content_id):
    stigma_info_url_template = base_url + "/content/info?app_sn=bh3_wiki&content_id={}"
    api_url = stigma_info_url_template.format(content_id)
    req = r.get(api_url)
    res = req.json()
    with open(os.path.join("./api", str(content_id) + ".json"), "w", encoding='utf8') as f:
        data = json.dumps(res, ensure_ascii=False, indent=4)
        f.write(data)
        print(data)


def get_all_stigma_info_from_api():
    with open("stigma_list_req.json", "r", encoding='utf-8') as f:
        res = json.loads(f.read())
    all_stigma_list = res['data']['list'][0]['list']
    error_content_id = []
    for item in all_stigma_list:
        content_id = item['content_id']
        try:
            get_single_stigma_from_api(content_id)
        except:
            print(traceback.format_exc())
            error_content_id.append(content_id)
            time.sleep(5)


def parse_stigma():
    all_file = os.listdir("./api")
    for file in all_file:
        with open(os.path.join("./api", file), "r", encoding='utf8') as f:
            res = json.loads(f.read())
            content = res['data']['content']
            parse_single_stigma(content)


def parse_single_stigma(content: dict):
    # print(content)
    global stigma_suit_start_id
    stigma = stigma_template.copy()
    stigma['item_id'] = content['id']
    stigma['name'] = str(content['title']).replace(" ", "")
    stigma['icon'] = content['icon']
    detail_content = content['contents']
    if len(detail_content) > 1:
        print("content id : {} has many contents")
        return
    detail_content = detail_content[0]
    detail_content_text = detail_content['text']
    soup = BeautifulSoup(detail_content_text, features="html.parser")
    all_td = soup.find_all("td")
    suit_name = ""
    suit_tag = ""
    suit_skill1_name = ""
    suit_skill2_name = ""
    for i in range(len(all_td)):
        td = all_td[i]
        value = td.text
        next_value = all_td[i + 1].text if i + 1 < len(all_td) else ""
        next_value = str(next_value).replace("\\t", "").replace("\\n", "").strip()
        if value == "圣痕技能":
            stigma["skill"] = next_value
        elif value == "所属套装":
            suit_name = stigma['suit_name'] = next_value
        elif value == "相关圣痕" and not stigma['image']:
            image_td = all_td[i + 2]
            image_url = image_td.next.attrs.get("src")
            stigma['image'] = image_url
        elif value == "套装tag":
            suit_tag = next_value
        elif value == "生命":
            stigma['hp'] = int(next_value) if next_value else 0
        elif value == "攻击":
            stigma['attack'] = int(next_value) if next_value else 0
        elif value == "防御":
            stigma['defence'] = int(next_value) if next_value else 0
        elif value == "会心":
            stigma['critical'] = int(next_value) if next_value else 0

    h3_tds = soup.find_all("td", {"class": "h3"})
    for i in range(len(h3_tds)):
        td = h3_tds[i]
        value = td.text
        if value == "10":
            stigma['star'] = 2
        elif value == "20":
            stigma['star'] = 3
        elif value == "30":
            stigma['star'] = 4
        elif value == '45':
            stigma['star'] = 5
        elif value == "相关圣痕":
            suit_skill1_name = str(h3_tds[i + 1].text).replace("\t", "").replace("\n", "").strip()
            suit_skill2_name = str(h3_tds[i + 2].text).replace("\t", "").replace("\n", "").strip()

    if suit_name and suit_name not in stigma_suit_map:
        # create new class
        stigma_suit = stigma_suit_template.copy()
        tds = soup.find_all("td", {"class": "obc-tmpl__rich-text"})
        if len(tds) > 2:
            stigma_suit["skill1_effect"] = tds[0].text.replace("\t", "").replace("\n", "").strip()
            stigma_suit["skill2_effect"] = tds[1].text.replace("\t", "").replace("\n", "").strip()
        stigma_suit['suit_id'] = stigma_suit_start_id
        stigma_suit_start_id += 1
        stigma_suit['name'] = suit_name
        stigma_suit['tag'] = suit_tag
        stigma_suit['skill1_name'] = suit_skill1_name
        stigma_suit['skill2_name'] = suit_skill2_name
        stigma_suit_map[suit_name] = stigma_suit
        print(stigma_suit)

    if suit_name is not None:
        stigma.pop("suit_name", "")
        suit_id = stigma_suit_map.get(suit_name, {}).get("suit_id", None)
        stigma['suit_id'] = suit_id

    stigma_list.append(stigma)


def to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['bh3']
    db['stigma'].insert_many(stigma_list)
    db['stigma_suit'].insert_many(stigma_suit_map.values())


if __name__ == "__main__":
    # get_stigma_list_from_api()
    # get_all_stigma_info_from_api()

    parse_stigma()
    to_mongo()
    print(stigma_list)
    print(stigma_suit_map)
    # with open(os.path.join("./api", "1841.json"), "r", encoding='utf8') as f:
    #     res = json.loads(f.read())
    #     content = res['data']['content']
    #     parse_single_stigma(content)
