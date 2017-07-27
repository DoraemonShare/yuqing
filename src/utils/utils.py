#-*-coding:utf-8 -*-


cartypeMap = {
    '"******************"': '"******************"',
    '"******************"': '"******************"',
    '"******************"': '"******************"',
    '"******************"': '"******************"'
}
#目前舆情分析中关注的列，列名来自postgresql数据表
concern_colcumns = ['topic', 'publicationDate', 'replyNum', 
                'clicks', 'postUrl', 'postContent', 'qaClassification', 'postType']
#excel的表头
EXCEL_HEADER = [u'贴名', u'发帖日期', u'回复数', u'点击数', u'贴URL', u'正文', u'算法标注结果']

not_concern_postType = ['icon_01', 'icon_02', 'icon_03', 'icon_04', 'icon_05',
                        'read-box', 'icon_04', 'icon-jian-grey', 'icon_business',
                        'icon-piao-grey', 'icon_buy', 'icon_video', 'icon_official',
                        'icon_zuan', 'icon_zhibo', 'icon_jing']

concern_postType = ['','icon_tu icon-tu-grey', 'icon_hot', 'icon_new', 'icon-wen-grey', None, 'None']

# -*- coding:utf-8 -*-
import csv
import codecs
# import pandas
import sys

# try to fix '_csv.Error: field larger than field limit (131072)'
csv.field_size_limit(sys.maxint) #field larger than field limit (131072)


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# # from  sqlalchemy.exc import OperationalError
# import psycopg2


# engine = create_engine('postgresql+psycopg2://postgres:oio@139.159.218.12:5432/postgres')
# engine = create_engine('postgresql+psycopg2://postgres:909@localhost:5432/postgres')

# session = sessionmaker(bind = engine)



sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']


def as_text(v):  ## 生成str, unicode字符串
    if v is None:
        return None
    elif isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):
        return v
    elif isinstance(v, unicode):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))



def read_by_line(filename=None, delimiter=',', field=None):
    '''
    to read csv file row by row (with Generator), with specified csv delimiter
    return specified fields or a whole csv-line
    params:
    csv_delimiter=',',csv delimiter, ',' default, 
    field=None, if None: return a whole csv line , if array, len(field) must be 1, or 2, if len(field)==1, return specified field, if len(field)==2, return line slice(include the end field)
    '''
    with codecs.open(filename, mode='rb', encoding='utf-8') as f:
        try:
            for row in f:
                row = row.split(delimiter)
                if field:
                    if len(field) == 1:
                        yield row[field[0]]
                    elif len(field) == 2:
                        yield row[field[0]:(field[1]+1)] #include the end field
                else:
                    yield row
        except Exception, e:
            raise


TOPICS = ['油耗', '操控', '最满意的一点', '最不满意的一点',
          '舒适性', '性价比', '内饰', '外观', '动力', '空间', '故障']

import pinyin

TOPICS_PINYIN = [pinyin.get(item, format='strip') for item in TOPICS]


import re
def cleaner(text):
    '''
    to clean text and return the text
    '''
    dirty_tag = ['&nbsp;', '\n', '=', '&nbsp', '&amp;', 'pos108', '\N',
                 '&amp', 'http://club.autohome.com.cn/bbs/thread-c-.+-.+.html；',
                 'http://club.autohome.com.cn/bbs/thread-c-.+-.+.html', '-', '\r']
    text = re.sub('|'.join(dirty_tag), '', text)
    if len(text) > 10:
        #去掉非中文
        if re.findall(u'[\u4e00-\u9fa5]+', text):
            return text
    else:
        return None
    # if text == '\n' or text == '&nbsp;' or text == '&nbsp\n':
    #     return
    # else:
    #     text = re.sub('|'.join(dirty_tag), '', text)
    #     return text




def str2unicode(s):
    '''
    将str转为unicode， utf8编码
    '''
    if isinstance(s, str):
        return unicode(s, 'utf-8')
    else:
        return s