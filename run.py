#-*-coding:utf-8 -*-

'''
启动pipeline
形式》》python run.py 2017-6-11 GS8
将分析6-11以后GS8的数据
'''


import sys
import os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))


from src.raw import loadData
# from src.preprocess import cleanData
from src.model import analysisData
from src.result import output2pg
from src.autowork.autowork import convert_csv_and_email

def main():
    try:
        if len(sys.argv) < 3:
            raise StandardError('please input date and car type, like 2017-6-8 GS8')
        else:
            wdate = sys.argv[1]
            wcar = sys.argv[2]
            # 下载数据
            raw_data_flpath = loadData.startup(w_date=wdate, w_car=wcar)
            if raw_data_flpath:
                # 分析，并返回文件名
                result_flpath = analysisData.startup(in_fl=raw_data_flpath)
                # 将分析结果写入postgres
                output2pg.startup(result_csv = result_flpath)
                # 将分析结果用EMAIL发送
                convert_csv_and_email(result_flpath)
        pass
    except Exception, e:
        print e
    finally:
        print 'run end...'

if __name__ == '__main__':
    main()