#-*-coding:utf-8 -*-

'''
--------------------------------------
@description:
1)整合csv转excel，并自动发送邮件
--------------------------------------
'''
import sys
import os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))


from src.utils.conf_email import MAIL_SERVER, FROM_ADDRESS, RECEIVER_ADDRESSES, LOGIN_PWD
from src.autowork import csv2excel
from src.autowork.automail import AutoSendEmail
from src.utils.info_path import local_data_prefix

def convert_csv_and_email(csv_result_fn):
    '''
    pass
    '''
    excel_fn = csv2excel.csv2xls(csv_result_fn)
    send_mail = AutoSendEmail(MAIL_SERVER, LOGIN_PWD, FROM_ADDRESS, RECEIVER_ADDRESSES)
    send_mail.send(filename=excel_fn)


def main():
    '''
    pass
    '''
    test_fn = local_data_prefix + 'result/result_autohome_bbsposts_where_wdate=2017-6-29_wcar=GS8.csv'
    convert_csv_and_email(test_fn)

if __name__ == '__main__':
    main()