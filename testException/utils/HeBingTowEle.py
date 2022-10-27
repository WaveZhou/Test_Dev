
list = [[1,'zhanggsan','12345',26],[6,'lisi','dsfdg',27],[2,'zhaoliu','65452',29],[5,'xuqi','5235',30],[3,'liba','52566',31],[4,'wangwu','12345',28],[9,'zhangjiu','15184',32],[7,'mashi','165484',88]]
list_temp = []
for i in range(len(list)):
    for j in range(i+1,len(list)):
        print(i,j)
        if list[i][2] == list[j][2]:
            temp_one = [4,'wagnwu','12345',list[i][3]+list[j][3]]
            list.remove(list[i])
            list.remove(list[j-1])
            temp_ele = list[j]
            temp_pre = list[j-1]
            list[j-1] = temp_one
            list[j] = temp_pre
            list.insert(j+1,temp_ele)
            list_temp.append(temp_ele)
            break
print(list)
"""
在list中的元素，list[2]的值相等时，合并这两个元素的某些属性的值，并把合并元素保留在list[2]相等的两元素位置的第二个元素的位置（删掉了原来list[2]值相等的两个元素）
"""