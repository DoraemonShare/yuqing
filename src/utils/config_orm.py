#-*-coding:utf-8 -*-

'''
postgresql configuration
table ORM
'''

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table, text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

engine = create_engine('*************************')
session = sessionmaker(bind = engine)

class BBSPost(Base):
    __tablename__ = 'autohome_bbsposts_specified'

    # id = Column(Integer(),primary_key=True)
    topic = Column(String()) #帖子名
    level = Column(String()) #帖子等级，加精、问帖。。。。
    writer = Column(String()) #发帖人
    publicationDate = Column(Date()) #发帖时间
    replyNum = Column(Integer()) #回复数 ---列表页与详情页不一定对得上
    clicks = Column(Integer())   #点击数 ---列表页与详情页不一定对得上
    finalReplyWriter = Column(String()) #最后回复人
    finalReplyDate = Column(Date()) #最后回复时间
    postUrl = Column(String(),primary_key=True) #详情页url
    qaClassification = Column(String()) #问答帖自带的分类，不一定准
    postContent = Column(String()) # 帖子正文
    postImageUrl = Column(String()) #帖子中图片的地址
    postType = Column(String()) #帖子的等级、类型，比如：提问贴，加精，有图贴等



# class BBSCarList(Base):
#     __tablename__ = 'autohome_bbscarlist_specified'

#     carType = Column(String()) #车型名
#     bbsUrl = Column(String(), primary_key=True) # 论坛地址
#     isUpdated = Column(Boolean()) #本次是否更新，用于控制是否需要爬这个分论坛key



class BBSPost_CLF(Base):
    __tablename__ = 'autohome_bbsposts_clf_results'

    # id = Column(Integer(),primary_key=True)
    topic = Column(String()) #帖子名
    # writer = Column(String()) #发帖人
    publicationDate = Column(Date()) #发帖时间
    replyNum = Column(Integer()) #回复数 ---列表页与详情页不一定对得上
    clicks = Column(Integer())   #点击数 ---列表页与详情页不一定对得上
    # finalReplyWriter = Column(String()) #最后回复人
    # finalReplyDate = Column(Date()) #最后回复时间
    postUrl = Column(String(),primary_key=True) #详情页url
    # qaClassification = Column(String()) #问答帖自带的分类，不一定准
    postContent = Column(String()) # 帖子正文
    # postImageUrl = Column(String()) #帖子中图片的地址
    # postType = Column(String()) #帖子的等级、类型，比如：提问贴，加精，有图贴等
    clfResult = Column(String()) #用模型判别出来的结果