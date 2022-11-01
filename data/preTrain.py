# coding=utf-8
import pandas as pd

result = open("wordlist.txt", 'w')

wordlist = pd.read_excel("COCA60000.xlsx", sheet_name="Sheet1")
print("Creating a word list...")
#   x is from 0 to 60022
#   In [x, y], the number of [x, 0] equals to (x + 2)
cnt = 0
for i in range(len(wordlist)):
    tmpWord = wordlist.iat[i, 2].lower()
    tmpWord = tmpWord[2:]
    print(i, tmpWord)
    if not 'a' <= tmpWord[0] <= 'z':
        continue
    else:
        printList = [tmpWord, " "]
        # A C D E I M P T U
        # J = adj N = n R = adv V = v
        tmpPos = str(wordlist.iat[i, 1])
        if tmpPos[1] == 'J':
            printList.append('a')
        elif tmpPos[1] == 'N':
            printList.append('n')
        elif tmpPos[1] == 'R':
            printList.append('r')
        elif tmpPos[1] == 'V':
            printList.append('v')
        else:
            continue
        printList.append(" ")
        printList.append(str(wordlist.iat[i, 3]))
        result.writelines(printList)
        result.write("\n")
print("The word list has been generated successfully")
result.close()
