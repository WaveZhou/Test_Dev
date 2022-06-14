# _*_ coding: utf-8 _*_
from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution
from Check_Bill_Test.utils.BatchDecompression import BatchDecompression


class YongAn(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == '永安' and self.type == '期货':
            bd = BatchDecompression(file_path, file_path, ['盯市'])
            bd.batchExt()
        # elif self.belong == '永安' and self.type == '普通':
        #     bd = BatchDecompression(file_path, file_path, ['699020', '699021', '699099'])
        #     bd.batchExt()
