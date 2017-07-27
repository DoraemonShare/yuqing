#-*-coding:utf-8 -*-

'''
将每天的模型判断结果写到数据库
'''

import fasttext
import codecs
import sys
import os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))

from src.utils.info_path import local_data_prefix
from src.utils.utils import read_by_line, concern_colcumns
from src.utils.config_orm import session, BBSPost_CLF


def check_validity(item=None, validity=None):
    '''
    校对结果有效性
    item: string，待检验的内容
    validity: string, 期待的type，如string， integer等
    '''
    if validity == 'int':
        if not item or item == 'None':
            return False
        else:
            return True
    elif validity == 'string':
        if not item or item == 'None':
            return False
        else:
            return True
    else:
        raise StandardError('not validity type...')

def build_orm_obj(contents):
    '''
    由文本构建可写入pg的orm对象
    如果原内容为'None' 或Null， 则orm obj那一列的内容为空
    '''
    clf_orm = BBSPost_CLF()
    if check_validity(contents[-1], 'string'):
        clf_orm.clfResult = contents[-1].strip()
    if check_validity(contents[concern_colcumns.index('topic')], 'string'):
        clf_orm.topic = contents[concern_colcumns.index('topic')]
    if check_validity(contents[concern_colcumns.index('publicationDate')], 'string'):
        clf_orm.publicationDate = contents[concern_colcumns.index('publicationDate')]
    if check_validity(contents[concern_colcumns.index('clicks')], 'int'):
        clf_orm.clicks = contents[concern_colcumns.index('clicks')]
    if check_validity(contents[concern_colcumns.index('postContent')], 'string'):
        clf_orm.postContent = contents[concern_colcumns.index('postContent')]
    if check_validity(contents[concern_colcumns.index('postUrl')], 'string'):
        clf_orm.postUrl = contents[concern_colcumns.index('postUrl')]
    if check_validity(contents[concern_colcumns.index('replyNum')], 'int'):
        clf_orm.replyNum = contents[concern_colcumns.index('replyNum')]

    return clf_orm



sess = session()


def startup(result_csv):
    count = 0
    try:
        for row in read_by_line(filename=result_csv, delimiter='|'):
            try:
                new_clf_result = build_orm_obj(row)
                a = sess.query(BBSPost_CLF).get(new_clf_result.postUrl)
                # print count
                # url = new_clf_result.postUrl
                # target = u'http://club.autohome.com.cn//bbs/thread-c-4094-63988189-1.html'
                # print url
                # if new_clf_result.postUrl == target:
                #     print new_clf_result.postUrl
                #     # print count
                #     print a
                if not a:
                    sess.add(new_clf_result)
                    count += 1
                if count % 100 == 0 and count != 0:
                    try:
                        sess.commit()
                        print 'add--%d--rows data' % count
                    except Exception, e:
                        print e
                        sess.rollback()
            except Exception, e:
                print e
        try:
            # 最后再提交一次，避免最后一批数据不满百而未被提交
            sess.commit()
        except Exception, e:
            print e
            sess.rollback()
    except Exception, e:
        print e
    finally:
        print "total num of rows to commit>> %d" % count
        sess.close()

            



def main():
    # r_csv = local_data_prefix + 'result/result_autohome_bbsposts_where_wdate=2017-6-1_wcar=GS8.csv'
    # startup(result_csv = r_csv)
    # r_csv = local_data_prefix + 'result/result_autohome_bbsposts_where_wdate=2017-6-5_wcar=GS8.csv'
    # startup(result_csv = r_csv)
    # r_csv = local_data_prefix + 'result/result_autohome_bbsposts_where_wdate=2017-6-8_wcar=GS8.csv'
    # startup(result_csv = r_csv)
    r_csv = local_data_prefix + 'result/test.csv'
    startup(result_csv = r_csv)

if __name__ == '__main__':
    main()
