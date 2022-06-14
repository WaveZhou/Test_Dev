from cnocr import CnOcr

with open("p2t.txt", "w") as f:
    ocr = CnOcr()
    pages = 1  # 上一步有多少页，这里就是多少
    n = 0
    for n in range(pages):
        i = 0
    j = 0
    name = './images/images_' + str(n + 1) + '.png'
    res = ocr.ocr(name)
    res2 = ocr.ocr_for_single_line(name)
    string_list = []
    for i in range(len(res)):
        for j in res[i]:
            string_list.append(j)
    ocr_result_string = "".join(string_list)
    print("Page ", str(n + 1))
    print(ocr_result_string)
    f.write(ocr_result_string)  # 这句话自带文件关闭功能，不需要再写f.close()
    print("转换结束。")
