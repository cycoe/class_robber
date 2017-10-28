#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import os


def getRandomTime(sleepTime):

    def wrapper():

        return sleepTime * (1 + random.random())

    return wrapper


class Config(object):
    """
    管理配置的类
    """

    refreshSleep = getRandomTime(5)   # 刷新的间隔时间
    wechatPushSleep = getRandomTime(1)     # 发送两条微信消息之间的间隔
    # wechatGroup_ = ['研究生的咸♂鱼生活']     # 讲座推送的微信群名称
    # wechatUser_ = ['邱大帅全宇宙粉丝后援会']  # 讲座推送的用户名称

    logPath = 'robber.log'
    userFile = 'password_'
    userName = ''
    password = ''

    @staticmethod
    def checkUserFile():
        return os.path.exists(Config.userFile)

    @staticmethod
    def readUserInfo():
        with open(Config.userFile) as fr:
            content = fr.readlines()
            Config.userName = content[0].strip()
            Config.password = content[1].strip()

    @staticmethod
    def dumpUserInfo():
        with open(Config.userFile, 'w') as fr:
            fr.write(Config.userName)
            fr.write('\n')
            fr.write(Config.password)

    @staticmethod
    def cleanUserInfo():
        if Config.checkUserFile():
            os.remove(Config.userFile)
