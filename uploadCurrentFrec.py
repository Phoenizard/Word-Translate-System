# coding=utf-8
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pandas import DataFrame
import enchant


def inputText(root):
    data = []
    try:
        file_in = open(root, 'r')  # Get txt article
        line = file_in.readline()
    except:
        file_in = open(root, 'r', encoding='utf-16')
        line = file_in.readline()
    line = line[:-1]
    data.append(line)
    while line:
        line = file_in.readline()
        line = line[:-1]
        data.append(line)
    file_in.close()
    # print(data)
    return data


def SortWord(word_table):
    StemmedWords = []
    StemmedWords_pos = []
    wnl = WordNetLemmatizer()
    for s in word_table:
        s = nltk.sent_tokenize(s)
        s = [word for word in s if word not in stopwords.words('english')]
        for sent in s:
            sw = nltk.pos_tag(nltk.word_tokenize(sent))
            for word_tub in sw:
                flag = 0
                for p in word_tub[0]:
                    if p == '\'':
                        flag = 1
                        break
                if flag == 1:
                    continue
                if word_tub[1] != 'NNP' and word_tub[1] != 'NNPS' and ('A' <= word_tub[1] <= 'Z'):
                    #  "n" for nouns,
                    #  "v" for verbs,
                    #  "a"  for adjectives
                    #  "r" for adverbs
                    if word_tub[1][0] == 'J':
                        # print(word_tub[0], word_tub[1], wnl.lemmatize(word_tub[0], 'a'))
                        StemmedWords.append(wnl.lemmatize(word_tub[0], 'a').lower())
                        StemmedWords_pos.append('a')
                    elif word_tub[1][0] == 'N':
                        # print(word_tub[0], word_tub[1], wnl.lemmatize(word_tub[0], 'n'))
                        StemmedWords.append(wnl.lemmatize(word_tub[0], 'n').lower())
                        StemmedWords_pos.append('n')
                    elif word_tub[1][0] == 'R':
                        # print(word_tub[0], word_tub[1], wnl.lemmatize(word_tub[0], 'r'))
                        StemmedWords.append(wnl.lemmatize(word_tub[0], 'r').lower())
                        StemmedWords_pos.append('r')
                    elif word_tub[1][0] == 'V':
                        # print(word_tub[0], word_tub[1], wnl.lemmatize(word_tub[0], 'v'))
                        StemmedWords.append(wnl.lemmatize(word_tub[0], 'v').lower())
                        StemmedWords_pos.append('v')
    # print(StemmedWords)
    stemmed_words = DataFrame(StemmedWords)
    stemmed_words.columns = ["Stemmed Words"]
    Pos_words = DataFrame(StemmedWords_pos)
    stemmed_words['PoS'] = Pos_words
    stemmed_words['Count'] = 1
    # print(stemmed_words)
    return stemmed_words


def analyzeProcess(stemmed_words):
    stemmed_words = stemmed_words.groupby(['Stemmed Words', 'PoS'], as_index=False).sum()
    uniqueWords = stemmed_words.sort_values(by="Count", ascending=False)
    uniqueWords = uniqueWords.reset_index(drop=True)
    print(uniqueWords)
    # 0 ------------word1 ----Frec2
    # ....
    # end ----------*---------1
    return uniqueWords


def outputText(uniqueWords, OutputRoot):
    freq_txt = open(OutputRoot, 'w')
    for i in range(len(uniqueWords)):
        flag = 0
        if len(str(uniqueWords["Stemmed Words"][i])) <= 1:
            continue
        for j in str(uniqueWords["Stemmed Words"][i]):
            if j == "*" or j == '.':
                flag = 1
                break
        if flag == 1:
            continue
        if not enchant.Dict("en_US").check(str(uniqueWords["Stemmed Words"][i])): # slow
            continue
        freq_txt.write(str(uniqueWords["Stemmed Words"][i]) + " " + str(uniqueWords["PoS"][i]) + " " + str(uniqueWords["Count"][i]))
        freq_txt.write("\n")


def ucf(rootIn, rootOut):
    print("----------------------------------")
    rs = analyzeProcess(SortWord(inputText(rootIn)))
    print("Generate successfully")
    outputText(rs, rootOut)
    print("Print successfully")
    print("----------------------------------")
