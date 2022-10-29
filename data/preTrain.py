import pandas as pd
import os

config_ranks = 59000
result = open("wordlist.txt", 'w')

wordlist = pd.read_excel("COCA60000.xlsx", sheet_name="Sheet1")
print("Creating a word list...")
print("The threshold for word frequency is ", config_ranks)
#   x is from 0 to 60022
#   In [x, y], the number of [x, 0] equals to (x + 2)
cnt = 0
for i in range(config_ranks - 2, 60023):
    tmpWord = wordlist.iat[i, 2].lower()
    tmpWord = tmpWord[2:]
    if not 'a' <= tmpWord[0] <= 'z':
        continue
    else:
        result.write(tmpWord)
        cnt += 1
        if cnt == 10:
            result.write("\n")
            cnt = 0
        else:
            result.write(" ")
print("The word list has been generated successfully")
os.system("WordTable.py")
result.close()
