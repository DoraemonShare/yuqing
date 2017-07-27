#-*-coding:utf-8 -*-

'''
从本地文件（csv）读入清洗后的数据，进行分析后写入本地另一个csv文件
'''

import fasttext
import codecs
import sys
import os
import re

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))



from src.utils.info_path import local_data_prefix
from src.utils.utils import read_by_line, not_concern_postType, concern_postType, concern_colcumns

from src.preprocess.preprocessData import fenci


def load_ft_model():
    '''
    to load fasttext model and return
    '''
    modelname = local_data_prefix + 'model/gzclf_0606_binary_clf.bin'
    return fasttext.load_model(modelname, encoding='utf-8', label_prefix="__label__")

ft_classifier = load_ft_model()


def get_qa_type(qatext):
    '''
    input ：qatext--string , 如"问题分类：哈弗 > 哈弗H6 Coupe > 保险年检  > 其他"
    return ： string， 如： “保险年检”
    若类别太粗则丢，如：
    input 问题分类：哈弗 > 哈弗H6 Coupe
    return： None
    注意： \xc2\xa0为Non-breaking space的东西，用于阻止在此处自动换行和阻止多个空格被压缩成一个，参考http://blog.csdn.net/Q_AN1314/article/details/52984573
    '''
    import re
    try:
        # qatext may be ’\n‘ or ’ ‘
        if qatext is None or len(qatext)<2:
            return None
        else:
            qa_l = qatext.split('>')
            if len(qa_l) > 2:
                return re.sub(' |\xc2\xa0|\xa0|\xc2', '', qa_l[2]) 
            else:
                return None
    except Exception, e:
        raise StandardError('error in analysisData.get_qa_type >> %s' % e)


def predict_with_ft_model(text):
    fenci_text = fenci(text)
    labels = ft_classifier.predict_proba([fenci_text])
    # label and probability, 如：[[(‘故障维修’, 0.57)]]
    return labels[0][0][0]


def analysizer(contents=None):
    '''
    contents: list
    实现主逻辑
    '''
    analysis_result = ''
    postType = contents[concern_colcumns.index('postType')].strip()
    if postType in not_concern_postType:
        analysis_result = u'非关注内容'
    elif postType in concern_postType:
        if postType == 'icon-wen-grey':
            typeFromContents = get_qa_type(contents[concern_colcumns.index('qaClassification')])
            if typeFromContents:
                analysis_result = typeFromContents
            else:
                t_c_text = contents[concern_colcumns.index('topic')]
                t_c_text = t_c_text + u'。'
                t_c_text = t_c_text + contents[concern_colcumns.index('postContent')]
                # t_c_text = contents[concern_colcumns.index('topic')] \
                #         + '。' + contents[concern_colcumns.index('postContent')]
                analysis_result = predict_with_ft_model(t_c_text)
        else:
            t_c_text = contents[concern_colcumns.index('topic')]
            t_c_text = t_c_text + u'。'
            t_c_text = t_c_text + contents[concern_colcumns.index('postContent')]
            analysis_result = predict_with_ft_model(t_c_text)
    else:
        analysis_result = u'暂时无法判定类别，请告诉程序猿'
    return analysis_result

def startup(in_fl=None):
    '''
    1)in_fl: string, the raw file to clean
    2) to clean and fenci
    '''
    out_fl = local_data_prefix + 'result/result_'+ os.path.basename(in_fl)
    with codecs.open(out_fl, mode='w+', encoding='utf-8') as f:
        for row in read_by_line(filename=in_fl, delimiter='|||'):
            try:
                predict_result = analysizer(row)
                row = [item.strip() for item in row]
                # 替换掉原文本中可能有的','、'|'，避免跟新的分隔符冲突
                row = [re.sub(r',|\|', u'，', item) for item in row]
                row.append(predict_result)
                f.write('|'.join(row))
                f.write('\n')
            except Exception, e:
                print e
    return out_fl

def main():
    # raw_f = local_data_prefix + 'raw/autohome_bbsposts_where_wdate=2017-6-5_wcar=GS8.csv'
    # raw_f = local_data_prefix + 'raw/autohome_bbsposts_where_wdate=2017-6-1_wcar=GS8.csv'
    # raw_f = local_data_prefix + 'raw/autohome_bbsposts_where_wdate=2017-6-8_wcar=GS8.csv'
    raw_f = local_data_prefix + 'raw/autohome_bbsposts_where_wdate=2017-6-11_wcar=GS8.csv'
    startup(raw_f)

if __name__ == '__main__':
    main()