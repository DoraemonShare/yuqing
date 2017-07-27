#-*-coding:utf-8 -*-

'''
--------------------------------------
@description:
1)EMAIL配置信息
--------------------------------------
'''
import time

MAIL_SERVER = "******************"
FROM_ADDRESS = "******************"
LOGIN_PWD = "******************"
_client_1 = "******************"
_client_2 = "******************"
_client_3 = "******************"
RECEIVER_ADDRESSES = [FROM_ADDRESS, _client_1, _client_2, _client_3]


_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
DEFUALT_SUBJECT = '%s"******************"' % _date
DEFUALT_EMAIL_BODY = '如题，请查收。\n\n如后续不想收到本邮件，请回复我，谢谢。'