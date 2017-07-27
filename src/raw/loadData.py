#-*-coding:utf-8 -*-

'''
从postgresql导入数据，按日期、指定论坛，存入本地
'''

import datetime
import re
import codecs
import sys
import os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))

from src.utils.config_orm import session
from src.utils.config_orm import BBSPost
from src.utils.info_path import local_data_prefix
from src.utils.utils import cartypeMap

from src.utils.utils import cleaner

def query(wdate=None, wcar = None):
    try:
        sess = session()
        # th = sess.query(BBSPost).filter(BBSPost.clicks>8000).all()
        # th = sess.query(BBSPost)\
        #     .filter(BBSPost.publicationDate > '2017-6-5')\
        #     .filter(BBSPost.clicks > 1000)\
        #     .filter(BBSPost.postUrl.like('%3121%'))\
        #     .order_by(BBSPost.publicationDate.desc())\
        #     .all()
        th = sess.query(BBSPost)\
            .filter(BBSPost.publicationDate > wdate)\
            .filter(BBSPost.postUrl.like('%'+cartypeMap[wcar]+'%'))\
            .order_by(BBSPost.publicationDate.desc())\
            .all()
        return th
    except Exception, e:
        print e
    finally:
        sess.close()

def gen_out_filename(wdate=None, wcar = None):
    o_f = local_data_prefix + 'raw/autohome_bbsposts_where_wdate='+wdate+'_wcar='+wcar+'.csv'
    return o_f

def clean_str(text):
    dirty_tag = ['&nbsp;', '\n', '=', '&nbsp', '&amp;', 'pos108', '\N',
                 '&amp', 'http://club.autohome.com.cn/bbs/thread-c-.+-.+.html；',
                 'http://club.autohome.com.cn/bbs/thread-c-.+-.+.html']
    text = re.sub('|'.join(dirty_tag), '', text)
    if text:
        return text
    else:
        return 'None'

def convert2str_or_cleanstr(item, column_name):
    if isinstance(item, str) or isinstance(item, unicode):
        if column_name == 'postUrl':
            return 'http://club.autohome.com.cn/'+item
        else:
            return clean_str(item)
    elif isinstance(item, datetime.date):
        return item.strftime('%Y-%m-%d')
    elif isinstance(item, int):
        return str(item)
    elif not item:
        return 'None'

def output(content=None, out_fn=None):
    from src.utils.utils import concern_colcumns
    with codecs.open(filename=out_fn, mode='w+', encoding='utf-8') as f:
        for item in content:
            if item:
                key_content =  [convert2str_or_cleanstr(getattr(item, i), i) for i in concern_colcumns]
                key_content = '|||'.join(key_content)
                f.write(key_content)
                f.write('\n')


def startup(w_date=None, w_car=None):
    '''
    w_date: string， 指定日期，if None ，get all data
    w_car： string， 指定车型， if None, get all data
    '''
    try:
        q_result = query(wdate=w_date, wcar=w_car)
        if q_result:
            ofn = gen_out_filename(wdate=w_date, wcar=w_car)
            output(q_result, ofn)
            return ofn
        else:
            with codecs.open(ofn, mode='w+') as f:
                f.write('there is no result for query w_date=%s and w_car=%s' %(w_date, w_car))
    except Exception, e:
        print e


def main():
    # if len(sys.argv) < 3:
    #     raise StandardError('please input the specified car and date, if to get all data, input None, None')
    # wdate = sys.argv[1]
    # wcar = sys.argv[2]
    wdate='2017-6-11'
    wcar='GS8'
    startup(w_date=wdate, w_car=wcar)

if __name__ == '__main__':
    main()
