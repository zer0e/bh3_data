import json,os
import openpyxl

def to_excel(filename):
    wb = openpyxl.Workbook()
    sheet = wb.get_active_sheet()
    sheet['A1'] = "作者"
    sheet['B1'] = "分数"
    sheet['C1'] = "av号"
    sheet['D1'] = "队长"
    sheet['E1'] = "队长星级"
    sheet['F1'] = "队长装备"
    sheet['G1'] = "队友1"
    sheet['H1'] = "队友1星级"
    sheet['I1'] = "队友1装备"
    sheet['J1'] = "队友2"
    sheet['K1'] = "队友2星级"
    sheet['L1'] = "队友2装备"
    sheet['M1'] = "人偶"
    sheet['N1'] = "人偶星级"

    with open(filename + ".json",'r',encoding="UTF-8") as f:
        load_dict = json.load(f)
        for i in range(len(load_dict)):
            sheet['A' + str(i+2)] = str(load_dict[i]['author'])
            sheet['B' + str(i+2)] = str(load_dict[i]['score'])
            sheet['C' + str(i+2)] = str(load_dict[i]['av'])
            sheet['D' + str(i+2)] = str(load_dict[i]['team01'])
            sheet['E' + str(i+2)] = str(load_dict[i]['team01_class'])
            sheet['F' + str(i+2)] = str(load_dict[i]['team01_equipment'])
            sheet['G' + str(i+2)] = str(load_dict[i]['team02'])
            sheet['H' + str(i+2)] = str(load_dict[i]['team02_class'])
            sheet['I' + str(i+2)] = str(load_dict[i]['team02_equipment'])
            sheet['J' + str(i+2)] = str(load_dict[i]['team03'])
            sheet['K' + str(i+2)] = str(load_dict[i]['team03_class'])
            sheet['L' + str(i+2)] = str(load_dict[i]['team03_equipment'])
            sheet['M' + str(i+2)] = str(load_dict[i]['figure'])
            sheet['N' + str(i+2)] = str(load_dict[i]['figure_star'])
        # print(load_dict)
    wb.save("./excel/" + filename + ".xlsx")


if __name__ == "__main__":
    if not os.path.exists("./excel/"):
        os.mkdir("./excel/")
    all_file = os.listdir('.')
    for file in all_file:
        if "json" in file:
            print(file[:-5])
            to_excel(file[:-5])