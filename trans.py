# -*- coding: UTF-8 -*-
import sys
import os
import requests
from requests.exceptions import RequestException
import uuid
import hashlib
import time
import pandas as pd
import enchant

CURRENT_PATH = os.path.abspath(__file__)
CURRENT_PATH = os.path.split(CURRENT_PATH)[0]

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
                outputText = []
                for e in explains:
                    tmp_cut = 0
                    if (e[0] != 'a') and (e[0] != 'v') and (e[0] != 'n'):
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
                    return outputText


def transTXT(root, src, rank_config,res):
    dataset = []
    f_word = open(src, 'r')
    while True:
        line = f_word.readline()
        if not line:
            break
        info = line.strip().split(" ")
        info[2] = int(info[2])
        dataset.append(info)
    dataset = pd.DataFrame(dataset)
    dataset.columns = ["Words", "PoS", "Count"]
    f_word.close()
    ifNeedTrans = {}
    for i in range(int(rank_config * len(dataset)), len(dataset)):
        if ifNeedTrans.__contains__(dataset["Words"][i]):
            continue
        else:
            if len(dataset["Words"][i]) > 3 and int(dataset["Count"][i]) >= 100:
                ifNeedTrans[dataset["Words"][i]] = 1
    # Prepare the dataset
    data = []
    try:
        f_in = open(root, 'r')  # Get txt article
        line = f_in.readline()
    except:
        f_in = open(root, 'r', encoding='utf-16')
        line = f_in.readline()
    line = line.strip()
    data.append(line.split(" "))
    while line:
        line = f_in.readline()
        line = line.strip()
        data.append(line.split(" "))
    f_in.close()
    # Import the article
    f_res = open(res, "w")
    for i in range(len(data)):
        tmp_trans = []
        tmp_index = []
        for j in range(len(data[i])):
            if ifNeedTrans.__contains__(data[i][j]):
                if enchant.Dict("en_US").check(str(data[i][j])):
                    del ifNeedTrans[data[i][j]]
                    tmp_trans.append(translateWord(data[i][j]))
                    tmp_index.append(j)
        for j in range(len(tmp_trans)):
            index_t = tmp_index[j]+1
            for k in tmp_trans:
                data[i].insert(index_t, k)
                index_t += 1
        print(data[i])
        for j in data[i]:
            try:
                print(j)
                if isinstance(j, list):
                    for k in j:
                        f_res.write(str(k))
                else:
                    f_res.write(j)
                    f_res.write(" ")
            except:
                continue
        f_res.write('\n')
    f_res.close()
    print("Mark Successfully")
    # Find words and Insert translation


# if __name__ == '__main__':
#     root = "/home/shay1138/Workshop/WordTranslateSystem/source/HarryPotter-demo.txt"
#     src = "/home/shay1138/Workshop/WordTranslateSystem/data/wordlist-test.txt"
#     res = "/home/shay1138/Workshop/WordTranslateSystem/result/res_HarryPotter.txt"
#     transTXT(root, src, 0.55, res)
