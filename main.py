# coding=utf-8
import argparse
import sys
import os
import requests
import uploadCurrentFrec as ucf
import CombineData as com
import trans

current_root = os.getcwd()
text_root = ""
result_word_root = ""
frequency_root = ""
result_article_root = ""
rank_config = 0.56


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, default=None)  # txt(file name in source)
    arges = parser.parse_args()
    # python3 main.py --text=res_HarryPotter.txt
    name = arges.text
    text_root = current_root + "/source/" + name
    result_word_root = current_root + "/runs/" + name
    result_article_root = current_root + "/result/res_" + name
    frequency_root = current_root + "/frec/frec_" + name
    src_root = current_root + "/data/wordlist-test.txt" # remember to change
    ucf.ucf(text_root, frequency_root)
    # Create txt frequency txt
    print("Update the database")
    com.combination(src_root, frequency_root)
    # Combine with the original one
    # combination(src, tmp)
    trans.transTXT(text_root, src_root, rank_config, result_article_root)
    # mark
