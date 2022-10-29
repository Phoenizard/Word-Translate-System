# -*- coding: UTF-8 -*-
import sys
import os
import requests
from requests.exceptions import RequestException
import json
import uuid
import hashlib
import time

CURRENT_PATH = os.path.abspath(__file__)
CURRENT_PATH = os.path.split(CURRENT_PATH)[0]

file_in = open("./source/HarryPotter-demo.txt", 'r')
# file_in = open("./source/HarryPotter.txt", 'r', encoding='utf-16')
wordlist = open("./runs/result.txt", 'w')
dict_words = {}
YOUDAO_API_URL = 'https://openapi.youdao.com/api'
YOUDAO_API_DOC = r'http://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6' \
                 r'%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB' \
                 r'%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html '

ERROR_CODE = {
    '0': '正常',
    '101': '缺少必填的参数,首先确保必填参数齐全，然后确认参数书写是否正确',
    '102': '不支持的语言类型',
    '103': '翻译文本过长',
    '104': '不支持的API类型',
    '105': '不支持的签名类型',
    '108': '应用ID无效，注册账号，登录后台创建应用和实例并完成绑定，可获得应用ID和应用密钥等信息',
    '105': '不支持的签名类型',
}

config_length = 0
SameWordTable = {"fraternisation": "fraternization", "organise": "organize", "organisation": "organization"}


def get_result(word):
    time_curtime = int(time.time())
    app_id = '2feacb89f486dc40'  # 这里填应用ID
    app_key = 'SSu7RjlCRtOBtKv7zKnBn4MfL8cmUans'  # 这里填应用密钥
    uu_id = uuid.uuid4()
    sign = hashlib.sha256(
        (app_id + word + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()  # sign生成
    data = {
        'q': word,
        'from': "auto",
        'to': "auto",
        'appKey': app_id,
        'salt': uu_id,
        'sign': sign,
        'signType': "v3",
        'curtime': time_curtime,
    }
    try:
        r = requests.get(YOUDAO_API_URL, params=data)
        return r.json()

    except RequestException as e:
        print('net error: %s' % e.message)
        sys.exit()


def translateWord(n):
    if SameWordTable.__contains__(n):
        n = SameWordTable[n]
    result = get_result(n)
    error_code = result['errorCode']
    if error_code == '0':
        if 'basic' in result:
            basic = result['basic']
            explains = basic['explains']
            if len(explains) > 0:
                for e in explains:
                    outputText = []
                    tmp_cut = 0
                    if (e[0] != 'a') and (e[0] != 'c') and (e[0] != 'p') and (e[0] != 'v') and (e[0] != 'n'):
                        continue
                    for i in range(len(e)):
                        if e[i] == '；':
                            tmp_cut = tmp_cut + 1
                        if tmp_cut == 2:
                            outputText.append(e[0:i])
                            break
                    if tmp_cut < 2:
                        outputText.append(e)
                if len(outputText) > 0:
                    print(n)
                    wordlist.write(n)
                    wordlist.write("\n")
                    for o in outputText:
                        print(o)
                        wordlist.write(o)
                        wordlist.write("\n")


def ReadAndSortTxt():
    flag = 0
    while True:
        lines = file_in.readline()
        if not lines:
            break
        else:
            lines = lines.split()
            for this_line in lines:
                tmp_word = this_line
                f = 0
                t = len(tmp_word) - 1
                while True:
                    if ('A' <= tmp_word[f] <= 'Z') or ('a' <= tmp_word[f] <= 'z'):
                        break
                    else:
                        f += 1
                    if f >= len(tmp_word):
                        flag = 1
                        break
                while True:
                    if ('A' <= tmp_word[t] <= 'Z') or ('a' <= tmp_word[t] <= 'z'):
                        break
                    else:
                        t -= 1
                    if t <= 0:
                        flag = 1
                        break
                if f > t:
                    flag = 1
                if flag:
                    flag = 0
                else:
                    tmp_key = tmp_word[f: t + 1]
                    form_key = tmp_key.split("-")
                    for k in form_key:
                        k = k.lower()
                        if not dict_words.__contains__(k):
                            is_find = False
                            try_word = [k + 's', k + 'es', k + 'ed', k + 'en']
                            for i in try_word:
                                if dict_words.__contains__(i):
                                    dict_words[i] += 1
                                    is_find = True
                                    break
                            if not is_find:
                                dict_words[k] = 1

                        else:
                            dict_words[k] += 1


if __name__ == '__main__':
    ReadAndSortTxt()
    config_length = int(input("输入长度阈值："))  # recommend 10
    for key in dict_words.keys():
        if dict_words[key] == 1:
            if len(key) >= config_length:
                translateWord(key)
            else:
                continue
    file_in.close()
    wordlist.close()
