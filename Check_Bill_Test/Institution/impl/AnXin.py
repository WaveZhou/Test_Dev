# _*_ coding: utf-8 _*_
import os

from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution
from Check_Bill_Test.utils.BatchDecompression import BatchDecompression


class AnXin(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == '安信' and self.type == '期货':
            bd = BatchDecompression(file_path, file_path, ['盯市'])
            bd.batchExt()


if __name__ == '__main__':
    ax = AnXin('中信', '普通')
    print(ax.type, '+', ax.belong)
