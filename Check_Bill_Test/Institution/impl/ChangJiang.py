# _*_ coding: utf-8 _*_
from Check_Bill_Test.Institution.AbstractInstitution import AbstractInstitution
from Check_Bill_Test.utils.BatchDecompression import BatchDecompression


class ChangJiang(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == '长江' and self.type == '期货':
            bd = BatchDecompression(file_path, file_path, ['550825.txt', '550826.txt','550825.TXT','550826.TXT'])
            bd.batchExt()


if __name__ == '__main__':
    institution_impl = eval('ChangJiang')('长江', '期货')
    path = r"D:\Users\Administrator\AppData\Local\Programs\PycharmWorkSpace\Test_Dev\testException\load_path"
    institution_impl.load_file_content_for_date(path)
    print(institution_impl)
