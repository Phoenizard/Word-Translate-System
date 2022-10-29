file_in = open("wordlist.txt", "r")

WordTable = {}


def readIn():
    while True:
        lines = file_in.readline()
        if not lines:
            break
        else:
            lines = lines.split()
            for this_line in lines:
                tmp_word = this_line
                WordTable[tmp_word] = 1
    print("Saved into WordTable successfully")


def if_InTheList(w):
    if WordTable.__contains__(w):
        return True
    else:
        return False


if __name__ == '__main__':
    readIn()
    print(WordTable.keys())
