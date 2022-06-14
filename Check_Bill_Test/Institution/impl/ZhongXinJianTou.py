# _*_ coding: utf-8 _*_
from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution


class ZhongXinJianTou(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        print("中信建投券商的加载实现方法")