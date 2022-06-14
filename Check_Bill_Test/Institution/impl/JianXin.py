# _*_ coding: utf-8 _*_
from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution
from Check_Bill_Test.utils.BatchDecompression import BatchDecompression


class JianXin(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == '建信' and self.type == '期货':
            bd = BatchDecompression(file_path, file_path, ['30000072.txt'])
            bd.batchExt()