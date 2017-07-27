#-*-coding:utf-8 -*-

'''
从本地文件（csv）读入数据，进行清洗、分词后写入本地另一个csv文件
'''

import codecs
import sys
import os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))

# from src.utils.info_path import local_data_prefix
# from src.utils.utils import read_by_line, cleaner

# def startup(in_fl=None):
#     '''
#     1)in_fl: string, the raw file to clean
#     2) to clean and fenci
#     '''
#     out_fl = local_data_prefix + 'cleaned/'+ os.path.basename(in_fl)
#     with codecs.open(out_fl, mode='w+', encoding='utf-8') as f:
#         for row in read_by_line(filename=in_fl, delimiter='|||'):

import thulac
thu = thulac.thulac(seg_only = True)

def fenci(text):
    item = thu.cut(text.encode('utf-8'), text=True) # type为str
    item = unicode(item, 'utf-8')
    return item


def main():
    pass

if __name__ == '__main__':
    main()