#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import threading

from modules.animation import wait_animation
from modules.ArgvsParser import ArgvsParser
from modules.Config import Config
from modules.FileUtils import check_file_exists, dump_table, load_table
from modules.Logger import Logger
from modules.MisUtils import MisUtils
from modules.OutputFormater import OutputFormater
from modules.Qrcode import Qrcode
from modules.Robber import Robber
from modules.StatusHandler import StatusHandler
from modules.String import String

#
#                            _ooOoo_
#                           o8888888o
#                           88" . "88
#                           (| -_- |)
#                           O\  =  /O
#                        ____/`---'\____
#                      .'  \\|     |//  `.
#                     /  \\|||  :  |||//  \
#                    /  _||||| -:- |||||-  \
#                    |   | \\\  -  /// |   |
#                    | \_|  ''\---/''  |   |
#                    \  .-\__  `-`  ___/-. /
#                  ___`. .'  /--.--\  `. . __
#               ."" '<  `.___\_<|>_/___.'  >'"".
#              | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#              \  \ `-.   \_ __\ /__ _/   .-` /  /
#         ======`-.____`-.___\_____/___.-`____.-'======
#                            `=---='
#        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      Buddha Bless, No Bug !


if sys.argv[1:] and sys.argv[1] == "--debug":
    robber = Robber(print)
else:
    robber = Robber(lambda x: None)
robber.init_spider()


def main():
    outputWelcome()
    initArgvs()
    outputHelp()
    cycle()


def initArgvs():
    ArgvsParser.connect(['help', 'h'], outputHelp)
    ArgvsParser.connect(['report', 'r'], rob_report)
    ArgvsParser.connect(['grade', 'g'], fetch_grade)
    ArgvsParser.connect(['add', 'a'], add_class_key)
    ArgvsParser.connect(['list', 'l'], list_class_key)
    ArgvsParser.connect(['delete', 'de'], delete_class_key)
    ArgvsParser.connect(['class', 'c'], rob_class)
    ArgvsParser.connect(['quit', 'q'], quit_)
    ArgvsParser.connect(['emailLogin', 'el'], emailLogin)
    ArgvsParser.connect(['donate', 'd'], donate)
    ArgvsParser.connect(['stop'], stop_report)
    ArgvsParser.connect(['status', 's'], get_status)


def cycle():
    while True:
        command = input(
            '[' + str(len([status for status in StatusHandler.status.values() if status])) + '] >>> ')
        if not ArgvsParser.run(command):
            print(Logger.log(String['wrong_argument'], level=Logger.warning))


def outputWelcome():
    print(OutputFormater.table([
        ['Class Robber ' + Config.version],
        ['By ' + Config.author],
        ['Site: cycoe.cc'],
        ['GitHub: https://github.com/cycoe/class_robber'],
        ['License: MIT 3.0']
    ], padding=5, horizontalSpacer=False))


def outputHelp():
    print(OutputFormater.table([
        ['command', 'abbr.', 'description'],
        ['help', 'h', 'print helps'],
        ['emailLogin', 'el', 'login email to send notification'],
        ['grade', 'g', 'grade fetching mode']
        ['report', 'r', 'report robbing mode'],
        ['class', 'c', 'class robbing mode'],
        ['add', 'a', 'add keys for class robbing'],
        ['delete', 'de', 'delete keys for class robbing'],
        ['list', 'l', 'list keys for class robbing'],
        ['donate', 'd', 'support developer a cup of coffee'],
        ['quit', 'q', 'quit robber']
    ], gravity=OutputFormater.center, padding=2))


def rob_report():
    if not StatusHandler.status['report']:
        StatusHandler.signal['report'] = True
        robber.login()
        threading.Thread(target=robber.robReport, args=(lambda: None,)).start()


def fetch_grade():
    if not StatusHandler.status['grade']:
        StatusHandler.signal['grade'] = True
        robber.login()
        threading.Thread(target=robber.fetchGrade, args=(
            lambda: None, lambda x: None,)).start()


def rob_class():
    robber.login()
    robber.rob_class()


def stop_report():
    StatusHandler.signal['report'] = False
    StatusHandler.signal['grade'] = False
    print(Logger.log('正在关闭所有后台任务... '), end='')
    wait_animation(StatusHandler.get_status('report'))


def get_status():
    process = list(StatusHandler.status.keys())
    status = ['running' if item else 'stop' for item in list(
        StatusHandler.status.values())]
    print(OutputFormater.table(list(zip(process, status)),
                               gravity=OutputFormater.left, padding=2))


def add_class_key():
    class_key = []
    if check_file_exists(Config.file_name['class_key_cache']):
        class_key = load_table(Config.file_name['class_key_cache'])
    key_ = []
    for i in range(10):
        key = input('please input {}th key\n> '.format(str(i + 1)))
        if key:
            key_.append(key)
        else:
            break
    class_key.append(key_)
    dump_table(class_key, Config.file_name['class_key_cache'])


def list_class_key():
    class_key = [[]]
    if check_file_exists(Config.file_name['class_key_cache']):
        class_key = load_table(Config.file_name['class_key_cache'])
    print('======================')
    print('\n'.join(['<{}> '.format(str(index + 1)) +
                     ', '.join(class_key[index]) for index in range(len(class_key))]))
    print('======================')
    return class_key


def delete_class_key():
    class_key = list_class_key()
    if not class_key:
        print('Class key list is empty')
        return False
    while True:
        choice = input('Input the number  of the key to delete\n> ')
        if not choice:
            break
        try:
            choice = int(choice)
        except ValueError as e:
            print('Not a number!')
            continue
        if 0 < choice <= len(class_key):
            del class_key[int(choice) - 1]
            dump_table(class_key, Config.file_name['class_key_cache'])
            break
        else:
            print('Index out of range!')
            continue

    return True


def emailLogin():
    robber.emailLogin()


def donate():
    Qrcode.create_qrcode_img()
    print(Logger.log(String['thanks_to_donate'], [
        '1. ' + String['wechat'],
        '2. ' + String['alipay'],
        '3. ' + String['not_now']]))
    while True:
        choice = input('> ')
        if choice == '1':
            Qrcode.show_qrcode(Config.file_name['wechat_qrcode_img'])
            print(Logger.log(String['thanks_to_support']))
            break
        elif choice == '2':
            Qrcode.show_qrcode(Config.file_name['alipay_qrcode_img'])
            print(Logger.log(String['thanks_to_support']))
            break
        elif choice == '3':
            print(Logger.log(String['remember_to_donate']))
            break
        else:
            print(Logger.log(String['wrong_argument'], level=Logger.warning))


def quit_():
    stop_report()
    robber.clean()
    print(Logger.log(String['site_cleaning'], [
          String['exiting']], level=Logger.error))
    exit(0)


if __name__ == "__main__":
    main()
