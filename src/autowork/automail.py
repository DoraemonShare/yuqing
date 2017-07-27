#-*-coding:utf-8 -*-

'''
--------------------------------------
@description:
1)自动发送邮件给gaei mail
2）参考：http://lizhenliang.blog.51cto.com/7876557/1875330
2）参考：http://blog.csdn.net/menglei8625/article/details/7721746
--------------------------------------
'''
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import parseaddr, formataddr
from email import encoders

import sys
import os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))
from src.utils.conf_email import MAIL_SERVER, FROM_ADDRESS, RECEIVER_ADDRESSES, LOGIN_PWD
from src.utils.conf_email import DEFUALT_SUBJECT, DEFUALT_EMAIL_BODY
from src.utils.info_path import local_data_prefix
from src.utils.utils import str2unicode


class AutoSendEmail(object):
    '''
    利用email module发邮件的类
    '''

    def __init__(self, mailserver, pwd, from_addr, receiver_addr):
        self.mailserver = mailserver
        self.pwd = pwd
        self.from_addr = from_addr
        self.receiver_addr = receiver_addr
        self.conn = None

    def attachment(self, attachment_fn):
        '''
        发送附件
        '''
        with open(attachment_fn.decode('utf-8'), 'rb') as f:
            # MIMEBase表示附件的对象
            mime = MIMEBase('text', 'txt', filename=attachment_fn)
            # filename是显示附件名字
            show_name = os.path.basename(attachment_fn)
            mime.add_header('Content-Disposition',
                            'attachment', filename=show_name.decode('utf-8'))
            # 获取附件内容
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            # 作为附件添加到邮件
        return mime

    def formatAddr(self, s):
        '''
        格式化邮件地址
        '''
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def build_msg(self, subject, msgbody, attachment_fn):
        '''
        构建消息体
        '''
        msg = MIMEMultipart()
        msg['From'] = self.formatAddr('大数据舆情 <%s>' % self.from_addr).encode()
        msg['To'] = ','.join(self.receiver_addr)
        if not subject:
            subject = DEFUALT_SUBJECT
        msg['Subject'] = Header(subject, 'utf-8').encode()
        if not msgbody:
            msgbody = DEFUALT_EMAIL_BODY
            # plain代表纯文本
        msg.attach(MIMEText(msgbody, 'plain', 'utf-8'))
        if attachment_fn:
            msg.attach(self.attachment(attachment_fn))
        return msg.as_string()

    def send(self, subject=None, msgbody=None, filename=None):
        '''
        发送EMAIL
        '''
        try:
            self.conn = SMTP(self.mailserver)
            self.conn.starttls()
            self.conn.login(self.from_addr, self.pwd)
            self.conn.sendmail(self.from_addr, self.receiver_addr,
                               self.build_msg(subject, msgbody, filename))
        except smtplib.SMTPException, e:
            print e


def startup():
    '''
    to start up project
    '''
    try:
        test_fn = local_data_prefix + 'result/result_autohome_bbsposts_where_wdate=2017-6-29_wcar=GS8.csv'
        # 中文失败
        # test_fn = local_data_prefix + 'result/excel/GS8_2017-6-29后汽车之家论坛帖子—算法分类结果.xls'
        test_email = AutoSendEmail(MAIL_SERVER, LOGIN_PWD, FROM_ADDRESS, RECEIVER_ADDRESSES)
        test_email.send(filename=test_fn)

    except smtplib.SMTPException, e:
        print e

def main():
    startup()

if __name__ == '__main__':
    main()


# def formatAddr(s):
#     '''
#     格式化邮件地址
#     '''
#     name, addr = parseaddr(s)
#     return formataddr((Header(name, 'utf-8').encode(), addr))

# def mail_connect(mail_server=MAIL_SERVER, pwd=LOGIN_PWD, from_addr=FROM_ADDRESS):
#     '''
#     建立TLS连接
#     '''
#     s = SMTP(mail_server)
#     s.starttls()
#     s.login(from_addr, pwd)
#     return s

# def send_attachment(body=None, attachment_fn=None, from_addr=FROM_ADDRESS, to_addr=RECEIVER_ADDRESSES, 
#                     _subject= DEFUALT_SUBJECT):
#     '''
#     发送附件
#     '''
#     msg = MIMEMultipart()
#     msg['From'] = formatAddr('大数据舆情 <%s>' % from_addr).encode()
#     msg['To'] = ','.join(to_addr)
#     msg['Subject'] = Header(DEFUALT_SUBJECT, 'utf-8').encode()
#     # plain代表纯文本
#     msg.attach(MIMEText(body, 'plain', 'utf-8'))
#     with open(attachment_fn,'rb') as f:
#         # MIMEBase表示附件的对象
#         mime = MIMEBase('text', 'txt', filename=attachment_fn)
#         # filename是显示附件名字
#         show_name = os.path.basename(attachment_fn)
#         mime.add_header('Content-Disposition', 'attachment', filename=show_name)
#         # 获取附件内容
#         # mime.set_payload(f.read(), charset='utf-8')
#         mime.set_payload(f.read())
#         encoders.encode_base64(mime)
#         # 作为附件添加到邮件
#         msg.attach(mime)
#     return msg.as_string()


# def msg_format(from_addr=FROM_ADDRESS,
#                to_addr=RECEIVER_ADDRESSES, _subject=DEFUALT_SUBJECT, _content=None):
#     """
#     组装SMTP默认的email主题样式
#     """
#     if not _content:
#         _content = u"这是一封测试邮件 from zgy,2333~~~".encode('gbk')  # 中文
#     _subject = str2unicode(_subject)
#     return 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(from_addr, to_addr, DEFUALT_SUBJECT, _content)


# def send_email(from_addr=FROM_ADDRESS, to_addr=RECEIVER_ADDRESSES):
#     '''
#     pass
#     '''
#     s = mail_connect()
#     # msg = msg_format()
#     test_fn = local_data_prefix + 'result/result_autohome_bbsposts_where_wdate=2017-6-29_wcar=GS8.csv'
#     test_body = '附件是测试数据, 请查收！'
#     msg = send_attachment(body = test_body, attachment_fn=test_fn)
#     s.sendmail(from_addr, to_addr, msg)



