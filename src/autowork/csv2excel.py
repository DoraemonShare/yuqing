#-*-coding:utf-8 -*-

'''
--------------------------------------
@description:
1)csv转excel
--------------------------------------
'''
import sys
import os
import xlwt

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))

from src.utils.utils import read_by_line, EXCEL_HEADER
from src.utils.info_path import local_data_prefix

def write_excel_header(_my_sheet):
    '''
    写表头，表头配置在utils EXCEL_HEADER中
    '''
    for _ind in range(len(EXCEL_HEADER)):
        # 写表头
        _my_sheet.write(0, _ind, EXCEL_HEADER[_ind])
    return _my_sheet

def gen_xls_name(_ori_name):
    '''
    生成excel文件名，将英文名改写为中文名
    _ori_name: str, 如'result_autohome_bbsposts_where_wdate=2017-6-29_wcar=GS8.csv'
    -----------------------------------
     中文失败，主要是去不掉文件名前的路径
    return: str, 'GS8_2017-6-29后汽车之家论坛帖子——算法分类结果.xls'
    -----------------------------------------------
    return : str, 'GS8_autohome_bbsposts_classified_by_machine-learning-model_since_2017-6-29.xls'
    '''
    _start_date = _ori_name.split("=")[1].split('_')[0]
    _car_type = _ori_name.split("=")[2].split('.')[0]
    xls_name = '%s_autohome_bbsposts_classified_by_machine-learning-model_since_%s.xls ' % (_car_type, _start_date)
    return xls_name

def csv2xls(csv_fn):
    '''
    实现csv file转 excel
    '''
    try:
        myexcel = xlwt.Workbook(encoding='utf-8')
        mysheet = myexcel.add_sheet('sheet1')
        mysheet = write_excel_header(mysheet)
        # 原csv中需要写入excel文件的列index
        l = 1 # 从第一行开始写起
        for row in read_by_line(filename=csv_fn, delimiter='|'):
            for i in range(6):
                # i为列序，仅需要前6列
                mysheet.write(l, i, row[i])
            last_col = row[-1].strip()
            mysheet.write(l, 6, last_col) #第7列，序号为6，为'算法标注结果'
            l += 1
        csv_base_fn = os.path.basename(csv_fn).split('.')[0]
        excel_fn = local_data_prefix + 'result/excel/' + gen_xls_name(csv_base_fn)
        myexcel.save(excel_fn)
        return excel_fn

    except Exception, e:
        print e
    

def startup():
    '''
    pass
    '''
    test_fn = local_data_prefix + 'result/result_autohome_bbsposts_where_wdate=2017-6-29_wcar=GS8.csv'
    csv2xls(test_fn)

def main():
    startup()

if __name__ == '__main__':
    main()