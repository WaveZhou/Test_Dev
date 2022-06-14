# _*_ coding: utf-8 _*_
from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution
from Check_Bill_Test.utils.BatchDecompression import BatchDecompression


class YinHe(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == '银河' and self.type == '普通':
            bd = BatchDecompression(file_path, file_path, ['上海久铭投资'])
            bd.batchExt()
        elif self.belong == '银河' and self.type == '期货':
            bd = BatchDecompression(file_path,file_path,['盯市'])
            bd.batchExt()