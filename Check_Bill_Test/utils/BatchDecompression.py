# coding=utf-8
import rarfile, os, re, shutil, zipfile
from os import listdir

# _*_ coding: utf-8 _*_
from Check_Bill_Test.utils.Transform_FileName import Transform_FileName

"""
@Author: Wave Zhou
"""


# param(压缩包所在文件夹的dir，指定压缩包解压后存放文件的位置，要从压缩包中匹配出的文件的文件名数组)
# return null
# @author周浪
class BatchDecompression(object):
    def __int__(self):
        super(BatchDecompression, self)

    def __init__(self, sourcedir, targetdir, sample):
        self.source = sourcedir
        self.target = targetdir
        self.sample = sample
        self.flag = None
        self.valid_file_list = list()
        self.origin_files = list()
        self.save_origin_other_files(sourcedir)
        self.date = ''

    def save_origin_other_files(self, sourcedir):
        for file_or_rar in os.listdir(sourcedir):
            if os.path.isfile(os.path.join(sourcedir, file_or_rar)) and str(file_or_rar)[-3:] not in (
                    'rar', 'RAR', 'ZIP', 'zip'):
                self.origin_files.append(file_or_rar)
                self.valid_file_list.append(file_or_rar)

    def batchExt(self):
        if len(self.sample) < 1:
            raise Exception('第三个参数数组不能为空')
        filenames = listdir(self.source)
        for file in filenames:
            if '行情' in file:
                continue
            if str(file)[-3:] not in (
                    'rar', 'RAR', 'ZIP', 'zip'):
                continue
            path1 = os.path.join(self.source, file)
            tf = Transform_FileName()
            temp_date = tf.get_date(file)
            if temp_date != '' or temp_date is not None:
                self.date = temp_date
            if file.endswith('rar'):
                rf = rarfile.RarFile(path1)  # 待解压文件
                rf.extractall(self.target)  # 解压指定文件路径
            elif file.endswith('zip'):
                zf = zipfile.ZipFile(path1)
                zf.extractall(self.target)
                zf.close()
        folders = listdir(self.target)
        if len(self.sample) == 1:
            pattern = r"" + self.sample[0]  # 指定匹配模板
            self.flag = True
            self.recursion_search(folders, pattern)

        else:
            for i in range(len(self.sample)):
                if i == len(self.sample) - 1:
                    self.flag = True  # 最后一次遍历清楚压缩包
                pattern = r"" + self.sample[i]
                self.recursion_search(folders, pattern)

        for fd in folders:  # 最后清楚多余文件夹和文件
            if os.path.isdir(os.path.join(self.target, fd)):
                shutil.rmtree(os.path.join(self.target, fd))
            elif fd not in self.valid_file_list:
                os.remove(os.path.join(self.target, fd))

    def recursion_search(self, folders, pattern):
        foders_tmp = folders[:]  # 为了避免数组中元素删除造成的指针跳位
        for fd in foders_tmp:
            if fd.endswith('rar') or fd.endswith('zip'):
                if self.flag:
                    os.remove(os.path.join(self.target, fd))
                    folders.remove(fd)
                continue
            elif os.path.isfile(os.path.join(self.target, fd)):
                if re.search(pattern, fd) and re.search(pattern, fd).group(0) == pattern:
                    self.valid_file_list.append(fd)
                continue
            path2 = os.path.join(self.target, fd)
            self.rec_find(path2, pattern)

    def rec_find(self, path2, pattern):  # 开始递归查找想保留的文件内容
        file_names = os.listdir(path2)
        for fs in file_names:
            if os.path.isdir(os.path.join(path2, fs)):
                self.rec_find(os.path.join(path2, fs), pattern)
            elif re.search(pattern, fs) and re.search(pattern, fs).group(0) == pattern:
                self.valid_file_list.append(fs)
                shutil.move(os.path.join(path2, fs), os.path.join(self.target, fs))

    def get_rename_file(self):
        self.batchExt()
        for file in os.listdir(self.target):
            if file in self.valid_file_list:
                if file not in self.origin_files:
                    os.rename(os.path.join(self.target, file), os.path.join(self.target, self.date + file))
    # def judge_includedir(self,f):
    #     temp = False
    #     if os.path.isdir(os.path.join(self.target,f)):
    #         temp = True
    #     return temp
    # def judge_includedir(self,folders):
    #     temp = False
    #     for f in folders:
    #         if os.path.isdir(os.path.join(self.target,f)):
    #             temp = True
    #     return temp
    # def deal_no_dir(self,files,pattern):
    #     for f in files:
    #         if  not (re.search(pattern, f) and re.search(pattern, f).group(0) == pattern):
    #             os.remove(os.path.join(self.target,f))
