
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
��list�е�Ԫ�أ�list[2]��ֵ���ʱ���ϲ�������Ԫ�ص�ĳЩ���Ե�ֵ�����Ѻϲ�Ԫ�ر�����list[2]��ȵ���Ԫ��λ�õĵڶ���Ԫ�ص�λ�ã�ɾ����ԭ��list[2]ֵ��ȵ�����Ԫ�أ�
"""