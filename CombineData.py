# coding=utf-8
import pandas


def combination(src, tmp):
    new_dataSet = []
    f_src = open(src, 'r')
    f_tmp = open(tmp, 'r')
    while True:
        line = f_tmp.readline()
        if not line:
            break
        info = line.strip().split(" ")
        info[2] = int(info[2])
        new_dataSet.append(info)
    while True:
        line = f_src.readline()
        if not line:
            break
        info = line.strip().split(" ")
        info[2] = int(info[2])
        new_dataSet.append(info)
    # print(new_dataSet)
    df_new_data = pandas.DataFrame(new_dataSet)
    df_new_data.columns = ["Words", "PoS", "Count"]
    df_new_data = df_new_data.groupby(["Words", "PoS"], as_index=False).sum()
    df_new_data = df_new_data.sort_values(by="Count", ascending=False)
    df_new_data = df_new_data.reset_index(drop=True)
    # print(df_new_data)
    f_update = open(src, 'w')
    for i in range(len(df_new_data)):
        # print(df_new_data["Words"][i], df_new_data["PoS"][i], df_new_data["Count"][i])
        f_update.write(str(df_new_data["Words"][i])+" "+str(df_new_data["PoS"][i])+" " + str(df_new_data["Count"][i]))
        f_update.write("\n")
    f_update.close()
    print("Update successfully")

# if __name__ == '__main__':
#     s = "/home/shay1138/Workshop/WordTranslateSystem/data/wordlist-test.txt"
#     n = "/home/shay1138/Workshop/WordTranslateSystem/frec/frec_HarryPotter-demo.txt"
#     # /home/shay1138/Workshop/WordTranslateSystem/frec/frec_HarryPotter-demo.txt
#     # /home/shay1138/Workshop/WordTranslateSystem/data/wordlist-test.txt
#     combination(s, n)
