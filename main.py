#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules.Robber import Robber
from modules.ArgvsParser import ArgvsParser
from modules.OutputFormater import OutputFormater
from modules.Logger import Logger
from modules.MisUtils import MisUtils
import pyqrcode

robber = Robber()


def main():
    outputWelcome()
    initArgvs()
    outputHelp()
    cycle()


def initArgvs():
    ArgvsParser.connect(['help', 'h'], outputHelp)
    ArgvsParser.connect(['speech', 's'], robSpeech)
    ArgvsParser.connect(['class', 'c'], robAllClass)
    # ArgvsParser.connect(['englishTest', 'et'], robEnglish)
    ArgvsParser.connect(['login', 'l'], login)
    # ArgvsParser.connect(['notifySpeech', 'ns'], notifySpeech)
    # ArgvsParser.connect(['wechatLogin', 'wl'], wechatLogin)
    ArgvsParser.connect(['quit', 'q'], quit_)
    ArgvsParser.connect(['emailLogin', 'el'], emailLogin)
    ArgvsParser.connect(['donate', 'd'], printQRCode)


def cycle():
    while True:
        command = input('>>> ')
        if not ArgvsParser.run(command):
            print(Logger.log('Wrong arguments detected!', level=Logger.error))


def outputWelcome():
    print(OutputFormater.table([
        ['Class Robber V 2.1'],
        ['By cycoe'],
        ['Site: cycoe.win'],
        ['License: MIT 3.0']
    ], padding=5, horizontalSpacer=False))


def outputHelp():
    print(OutputFormater.table([
        ['command', 'abbr.', 'description'],
        ['help', 'h', 'print helps'],
        ['login', 'l', 'login web'],
        ['emailLogin', 'el', 'login email to send notification'],
        ['speech', 's', 'speech robbing mode'],
        # ['class', 'c', 'class robbing mode'],
        ['donate', 'd', 'support developer a cup of coffee'],
        ['quit', 'q', 'quit robber']
    ], gravity=OutputFormater.center, padding=2))


def login():
    robber.login()


def wechatLogin():
    robber.wechatLogin()


def robAllClass():
    robber.getClassIdList(None)


def notifySpeech():
    robber.notifySpeech()


def robSpeech():
    robber.robSpeech()


# def robClass():
#     robber.getClassIdList(argvsParser.listFile)


def robEnglish():
    robber.robEnglishTest()


def emailLogin():
    robber.emailLogin()


def printQRCode():
    wechatURI = pyqrcode.create(MisUtils.wechatURI)
    alipayURI = pyqrcode.create(MisUtils.alipayURI)
    print(Logger.log('Thanks a lot for donating'))
    print(OutputFormater.table([['Via wechat'], ['|'], ['V']], verticalSpacer=False, horizontalSpacer=False, padding=10))
    print(wechatURI.terminal(quiet_zone=1))
    print(OutputFormater.table([['Via alipay'], ['|'], ['V']], verticalSpacer=False, horizontalSpacer=False, padding=10))
    print(alipayURI.terminal(quiet_zone=1))


def quit_():
    robber.clean()


if __name__ == "__main__":
    main()
