# _*_ coding: utf-8 _*_
from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution
from Check_Bill_Test.utils.BatchDecompression import BatchDecompression


class GuoJun(AbstractInstitution):

    def load_file_content_for_date(self, file_path:str):
        if self.belong == '国君' and self.type == '普通':
            bd = BatchDecompression(file_path, file_path, ['.xlsx','.XLS'])
            bd.get_rename_file()
        if self.belong == '国君' and self.type == '期权':
            bd = BatchDecompression(file_path,file_path,['.pdf'])
            bd.batchExt()