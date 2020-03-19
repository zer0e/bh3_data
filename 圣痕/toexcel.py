import json
import openpyxl

def stig_to_xlsx():
    wb = openpyxl.Workbook()
    sheet = wb.get_active_sheet()
    sheet['A1'] = "圣痕名称"
    sheet['B1'] = "圣痕套装"
    sheet['C1'] = "圣痕图片地址"
    sheet['D1'] = "圣痕生命值"
    sheet['E1'] = "圣痕攻击力"
    sheet['F1'] = "圣痕防御值"
    sheet['G1'] = "圣痕会心值"
    sheet['H1'] = "圣痕技能"
    with open("stigma.json",'r',encoding="UTF-8") as f:
        load_dict = json.load(f)
        for i in range(len(load_dict)):
            sheet['A' + str(i+2)] = str(load_dict[i]['stig_name'])
            sheet['B' + str(i+2)] = str(load_dict[i]['stig_class'])
            sheet['C' + str(i+2)] = str(load_dict[i]['stig_img'])
            sheet['D' + str(i+2)] = str(load_dict[i]['stig_hp'])
            sheet['E' + str(i+2)] = str(load_dict[i]['stig_attack'])
            sheet['F' + str(i+2)] = str(load_dict[i]['stig_def'])
            sheet['G' + str(i+2)] = str(load_dict[i]['stig_huixin'])
            sheet['H' + str(i+2)] = str(load_dict[i]['stig_skill'])
        # print(load_dict)
    print("ok")
    wb.save("stigma.xlsx")


def stig_class_to_xlsx():
    wb = openpyxl.Workbook()
    sheet = wb.get_active_sheet()
    sheet['A1'] = "圣痕套装名称"
    sheet['B1'] = "圣痕星级"
    sheet['C1'] = "圣痕获取方式"
    sheet['D1'] = "圣痕介绍"
    sheet['E1'] = "圣痕图片1"
    sheet['F1'] = "圣痕图片2"
    sheet['G1'] = "两件套技能"
    sheet['H1'] = "三件套技能"
    with open("stigma_class.json",'r',encoding="UTF-8") as f:
        load_dict = json.load(f)
        for i in range(len(load_dict)):
            sheet['A' + str(i+2)] = str(load_dict[i]['stig_class_name'])
            sheet['B' + str(i+2)] = str(load_dict[i]['stig_class_star'])
            sheet['C' + str(i+2)] = str(load_dict[i]['get_function'])
            sheet['D' + str(i+2)] = str(load_dict[i]['stig_class_intro'])
            sheet['E' + str(i+2)] = str(load_dict[i]['stig_class_img1'])
            sheet['F' + str(i+2)] = str(load_dict[i]['stig_class_img2'])
            sheet['G' + str(i+2)] = str(load_dict[i]['two_stig_skill'])
            sheet['H' + str(i+2)] = str(load_dict[i]['three_stig_skill'])
    print("ok")
    wb.save("stigma_class.xlsx")
if __name__ == "__main__":
    stig_to_xlsx()
    stig_class_to_xlsx()