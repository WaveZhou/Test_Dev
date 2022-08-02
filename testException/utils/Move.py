# _*_ coding: utf-8 _*_
import os,shutil

class Auto_Increment:
    def __init__(self):
        self.num = 0
        self.target_file = None
        self.target_pre_file = None

    def get_add_one(self):
        self.num += 1
        return self.num

    def set_target_file(self, file: str):
        self.target_file = file

    def set_target_pre_file(self, file: str):
        self.target_pre_file = file


def rename_to_new_dir(origin_path, target_path, re_file_name, signal, flag):
    """
    源目录下的文件拷贝或剪切到目标目录，并更换目标目录的文件名
    :param origin_path: 源目录（精确到文件）
    :param target_path: 目标目录（只到目录）
    :param re_file_name: 新文件名名
    :param signal: 信号，1. 为拷贝， 2. 为剪切
    :param flag:目标目录文件已存在 增量为True,替换为False
    :return:Auto_Increment类的对象
    """
    # old_path = os.path.join(settings['origin_path'], institution, file_name)
    # new_path_parent = os.path.join(settings['not_matched'], date_str, dir_name)
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True),
    new_path = os.path.join(target_path, re_file_name)
    ai = Auto_Increment()
    count = 0
    if flag:
        map_dict = dict()
        while os.path.exists(new_path):
            new_path = os.path.join(target_path, re_file_name.split('.')[0] + '(' + str(ai.get_add_one()) + ').' +
                                    re_file_name.split('.')[1])
            map_dict[count] = new_path.split('\\')[-1]
            count += 1
        target_file = new_path.split('\\')[-1]
        ai.set_target_file(str(target_file))
        if count >= 2:
            ai.set_target_pre_file(str(map_dict[count - 2]))
    else:
        if os.path.exists(new_path):
            os.remove(new_path)
    if signal == 1:
        shutil.copy(origin_path, new_path)
    elif signal == 2:
        os.rename(origin_path, new_path)
    return ai
if __name__ == '__main__':
    orgin_path = r'D:\Users\Desktop\mails\target'
    for files_dir in os.listdir(os.path.join(orgin_path)):
        print(files_dir)