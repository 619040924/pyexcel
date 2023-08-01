import os.path
import re
import time

import openpyxl
import pandas

# # 打开Excel文件
# workbook = openpyxl.load_workbook("模板.xlsx")
#
# # 选择要操作的工作表
# worksheet = workbook.active
#
# # 向单元格写入数据
# worksheet["A1"] = "Hello"
#
# # 保存文件
# workbook.save("data.xlsx")

def sepnumber(num):
    try:
        num = float(num)
        ones = num % 10
        tens = (num // 10) % 10
        hundreds = (num // 100) % 10
        thousands = (num // 1000) % 10
        ten_thousands = (num // 10000) % 10
        hundred_thousands = (num // 100000) % 10
        return int(ones),int(tens),int(hundreds),int(thousands),int(ten_thousands),int(hundred_thousands)
    except Exception as e:
        return 0,0,0,0,0,0

def parse_data(ij):


    data_mumber = ij["编号"]
    data_sqsj = time.strptime(ij['申请时间'].split(" ")[0],'%Y年%m月%d日')
    if str(data_sqsj) == 'nan':
        year,mouth,day = '','',''
    else:
        year,mouth,day = time.strftime('%Y',data_sqsj),time.strftime('%m',data_sqsj),time.strftime('%d',data_sqsj)
    use_car_xz = ij['用车性质']

    to_local_path = f'./result/编号_{data_mumber}.xlsx'
    workbook = openpyxl.load_workbook("模板.xlsx")
    worksheet = workbook.active

    worksheet["A2"] = f"编号                                        申请日期：   {year}年  {mouth}月  {day}日"
    worksheet['D3'] = "北京大兴国际机场海关"
    if '执法执勤' in use_car_xz:
        worksheet["D4"] = '□ 执法执勤√       □ 应急保障     □ 机要通信   □ 离退休保障'
    elif '应急保障' in use_car_xz:
        worksheet["D4"] = '□ 执法执勤      □ 应急保障√     □ 机要通信   □ 离退休保障'
    elif '机要通信' in use_car_xz:
        worksheet["D4"] = '□ 执法执勤      □ 应急保障     □ 机要通信√   □ 离退休保障'
    elif '离退休保障' in use_car_xz:
        worksheet["D4"] = '□ 执法执勤      □ 应急保障     □ 机要通信   □ 离退休保障√'



    use_car_time = ij["用车时间"]
    data_sqsj = time.strptime(use_car_time,'%Y年%m月%d日 %H:%M')
    if str(data_sqsj) == 'nan':
        year,mouth,day,house,minute = '','','','',''
    else:
        year,mouth,day,house,minute = (
            time.strftime('%Y', data_sqsj),
            time.strftime('%m', data_sqsj),
            time.strftime('%d', data_sqsj),
            time.strftime('%H', data_sqsj),
            time.strftime('%M', data_sqsj)
        )
    worksheet["D7"] = f"{year}年"
    worksheet["G7"] = f"{mouth}月"
    worksheet["I7"] = f"{day}日"
    worksheet["K7"] = f"{house}时"
    worksheet["M7"] = f"{minute}分"

    worksheet["D8"] = ij["始发地点"] if str(ij["始发地点"])  != 'nan' else ''
    worksheet["D9"] = ij["目的地"] if str(ij["目的地"]) != 'nan' else ''
    worksheet["D5"] = ij["具体用车事由"] if str(ij["具体用车事由"]) != 'nan' else ''

    cf_plase_ = ij["出车地点"] if str(ij["出车地点"])  != 'nan' else ''
    hc_place = ij["回车地点"] if str(ij["回车地点"])  != 'nan' else ''

    ch_data =ij["始发地点"] if str(ij["始发地点"])  != 'nan' else ''
    mdd_data = ij["目的地"] if str(ij["目的地"])  != 'nan' else ''

    if cf_plase_ == '' or hc_place == "":
        pass
    elif cf_plase_ == hc_place:
        worksheet["D10"] = '□单程    □往返√'
        worksheet["B17"] = f'行驶轨迹：{ch_data} 到 {mdd_data} 到 {ch_data}'

    else:
        worksheet["D10"] = '□单程√    □往返'
        worksheet["B17"] = f'行驶轨迹：{ch_data} 到 {mdd_data}'

    nb_use_pepole = len([j for j in ij["内部乘车人"].split(",") if j.strip() != '']  ) if str(ij["内部乘车人"])  != 'nan' else 0
    wb_use_pepole = len([j for j in ij["其他乘车人"].split(",") if j.strip() != '']) if str(ij["其他乘车人"])  != 'nan' else 0
    tot_use_pepole = nb_use_pepole + wb_use_pepole
    worksheet["D11"] = str(tot_use_pepole)
    worksheet["D12"] = ij["申请人"] if str(ij["申请人"])  != 'nan' else ''
    worksheet["H11"] = ij["审批人"] if str(ij["审批人"]) != 'nan' else ''
    worksheet["D13"] = ""
    worksheet["B15"] = f'驾 驶 员：{ij["驾驶人"]}' if str(ij["驾驶人"]) != 'nan' else ''

    sp_car_INFO = ij["实派车辆"] if str(ij["实派车辆"])  != 'nan' else ''
    sp_cx = ''.join(re.findall(r'\((.*?)\)',sp_car_INFO))
    sp_cp = sp_car_INFO.split("(")[0]
    worksheet["G15"] = f'车型：{sp_cx}'
    worksheet["J15"] = f'车牌号码：{sp_cp}'

    worksheet["B16"] = ij["驾驶人"] if str(ij["驾驶人"]) != 'nan' else ''
    cclc = ij["出车里程"] if str(ij["出车里程"]) != 'nan' else ''
    hundred_thousands, ten_thousands, thousands, hundreds, tens, ones = sepnumber(cclc)
    worksheet["I16"] = str(ones)
    worksheet["J16"] = str(tens)
    worksheet["K16"] = str(hundreds)
    worksheet["L16"] = str(thousands)
    worksheet["M16"] = str(ten_thousands)
    worksheet["N16"] = str(hundred_thousands)

    worksheet["B20"] = f'总行驶里程：{ij["核实里程(公里)"]}' if str(ij["核实里程(公里)"]) != 'nan' else ''
    worksheet["D21"] = f'{ij["设备上报耗油量(升)"]}' if str(ij["设备上报耗油量(升)"]) != 'nan' else ''
    worksheet["G21"] = f'费用：{ij["参考油费(元)"]}' if str(ij["参考油费(元)"]) != 'nan' else ''


    hclc = ij["回车里程"] if str(ij["回车里程"]) != 'nan' else ''
    hundred_thousands, ten_thousands, thousands, hundreds, tens, ones = sepnumber(hclc)
    worksheet["I20"] = str(ones)
    worksheet["J20"] = str(tens)
    worksheet["K20"] = str(hundreds)
    worksheet["L20"] = str(thousands)
    worksheet["M20"] = str(ten_thousands)
    worksheet["N20"] = str(hundred_thousands)

    worksheet["B22"] = f'驾驶员签字: {ij["驾驶人"]}' if str(ij["驾驶人"]) != 'nan' else ''
    worksheet["H22"] = f'派车人签字：{ij["派车人"]}' if str(ij["派车人"]) != 'nan' else ''

    workbook.save(to_local_path)







if  __name__ == "__main__":
    try:

        if not os.path.exists("./result"):
            os.makedirs("./result")

        records = pandas.read_excel("输入表.xlsx", header=1).to_dict(orient='records')
        for ij in records[:]:
            try:
                print(ij)
                parse_data(ij)
            except Exception as e:
                print(f"解析异常：{e}")
                time.sleep(1)

        input(">>> 解析结束！")
    except Exception as e:
        input(">>> 解析异常！")