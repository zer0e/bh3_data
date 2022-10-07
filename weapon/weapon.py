import copy
import json
import os
import time
import traceback
import pymongo

import requests as r
from bs4 import BeautifulSoup

base_url = "https://api-static.mihoyo.com/common/blackboard/bh3_wiki/v1"

weapon_template = {
    'item_id': "", "name": "", "attack": 0, "critical": 0, "star": 0, "introduction": "",
    "icon": "", "image": "", "skill_list": []
}

skill_template = {
    "name": "",
    "effect": ""
}
weapon_list = []


def get_weapon_list_from_api():
    stigma_list_url = base_url + "/home/content/list?app_sn=bh3_wiki&channel_id=20"
    req = r.get(stigma_list_url)
    res = req.json()
    with open("weapon_list_req.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))


def get_single_weapon_from_api(content_id):
    stigma_info_url_template = base_url + "/content/info?app_sn=bh3_wiki&content_id={}"
    api_url = stigma_info_url_template.format(content_id)
    req = r.get(api_url)
    res = req.json()
    with open(os.path.join("./api", str(content_id) + ".json"), "w", encoding='utf8') as f:
        data = json.dumps(res, ensure_ascii=False, indent=4)
        f.write(data)
        print(data)


def get_all_weapon_info_from_api():
    with open("weapon_list_req.json", "r", encoding='utf-8') as f:
        res = json.loads(f.read())
    all_stigma_list = res['data']['list'][0]['list']
    error_content_id = []
    for item in all_stigma_list:
        content_id = item['content_id']
        try:
            get_single_weapon_from_api(content_id)
        except:
            print(traceback.format_exc())
            error_content_id.append(content_id)
            time.sleep(5)


def parse_single_weapon(content: dict):
    weapon = copy.deepcopy(weapon_template)
    weapon['item_id'] = content['id']
    weapon['name'] = str(content['title']).strip()
    weapon['icon'] = content['icon']
    detail_content = content['contents']
    detail_content = detail_content[0]
    detail_content_text = detail_content['text']
    soup = BeautifulSoup(detail_content_text, features="html.parser")
    all_td = soup.find_all("td")
    for i in range(len(all_td)):
        td = all_td[i]
        td_text = td.text
        next_td = all_td[i + 1] if i + 1 < len(all_td) else None
        next_td_text = next_td.text if next_td else ""
        if td_text == "攻击":
            weapon['attack'] = int(next_td_text) if next_td_text else 0
        elif td_text == '会心':
            weapon['critical'] = int(next_td_text) if next_td_text else 0

    star_icon = soup.find_all("i", {"class": "obc-tmpl__rate-icon"})
    weapon['star'] = len(star_icon)
    desc_div = soup.find_all("div", {"class": "obc-tmpl-weapon__info-desc"})
    if desc_div:
        text_list = [str(div.text).strip() for div in desc_div]
        weapon['introduction'] = "\n".join(text_list)

    skill_div = soup.find_all("div", {"data-part": "skill"})
    if skill_div:
        skill_div = skill_div[0]
        tds = skill_div.find_all("td")
        for i in range(0, len(tds), 2):
            skill = skill_template.copy()
            skill['name'] = str(tds[i].text).replace("\n", "").replace("\t", "").strip()
            skill['effect'] = str(tds[i + 1].text).replace("\n", "").replace("\t", "").strip()
            weapon['skill_list'].append(skill)
    weapon_list.append(weapon)
    print(weapon)


def parse_weapon():
    all_file = os.listdir("./api")
    for file in all_file:
        with open(os.path.join("./api", file), "r", encoding='utf8') as f:
            res = json.loads(f.read())
            content = res['data']['content']
            parse_single_weapon(content)


def test():
    with open(os.path.join("./api", "76.json"), "r", encoding='utf8') as f:
        res = json.loads(f.read())
        content = res['data']['content']
        parse_single_weapon(content)


def to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['bh3']
    db['weapon'].insert_many(weapon_list)


if __name__ == '__main__':
    # get_weapon_list_from_api()
    # get_all_weapon_info_from_api()
    parse_weapon()
    to_mongo()
