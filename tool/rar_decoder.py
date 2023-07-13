#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from unrar import rarfile


def rar_cracking(filename):
    fp = rarfile.RarFile('test.rar')
    fpPwd = open('pwd.txt')
    for pwd in fpPwd:
        pwd = pwd.rstrip()
        try:
            fp.extractall(path='test', pwd=pwd.encode())
            print('[+] Find the password: ' + pwd)
            fp.close()
            break
        except:
            pass
    fpPwd.close()


if __name__ == '__main__':
    filename = r'C:\迅雷下载\S09\1-7\1-7.rar'
    if os.path.isfile(filename) and filename.endswith('.rar'):
        rar_cracking(filename)
    else:
        print('Not a rar file')