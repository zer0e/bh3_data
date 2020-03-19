import json
import openpyxl

def get_weapon_class(class_id):
    if class_id == 1:
        return "双枪"
    if class_id == 2:
        return "太刀"
    if class_id == 3:
        return "重炮"
    if class_id == 4:
        return "大剑"

    if class_id == 5:
        return "十字架"

    if class_id == 6:
        return "拳套"
    if class_id == 7:
        return "镰刀"


def weapon_to_excel():
    wb = openpyxl.Workbook()
    sheet = wb.get_active_sheet()
    sheet['A1'] = "武器名称"
    sheet['B1'] = "武器星级"
    sheet['C1'] = "武器介绍"
    sheet['D1'] = "武器分类"
    sheet['E1'] = "武器图片"
    sheet['F1'] = "武器攻击力"
    sheet['G1'] = "武器会心值"
    sheet['H1'] = "武器技能1"
    sheet['I1'] = "武器技能2"
    sheet['J1'] = "武器技能3"
    with open("weapon.json",'r',encoding="UTF-8") as f:
        load_dict = json.load(f)
        for i in range(len(load_dict)):
            sheet['A' + str(i+2)] = str(load_dict[i]['weapon_name'])
            sheet['B' + str(i+2)] = str(load_dict[i]['weapon_star'])
            sheet['C' + str(i+2)] = str(load_dict[i]['weapon_intro'])
            sheet['D' + str(i+2)] = get_weapon_class(load_dict[i]['weapon_class'])
            sheet['E' + str(i+2)] = str(load_dict[i]['weapon_img'])
            sheet['F' + str(i+2)] = str(load_dict[i]['weapon_attack'])
            sheet['G' + str(i+2)] = str(load_dict[i]['weapon_huixin'])
            sheet['H' + str(i+2)] = str(load_dict[i]['skill1'])
            sheet['I' + str(i+2)] = str(load_dict[i]['skill2'])
            sheet['J' + str(i+2)] = str(load_dict[i]['skill3'])
        # print(load_dict)
    print("ok")
    wb.save("weapon.xlsx")

if __name__ == "__main__":
    weapon_to_excel()