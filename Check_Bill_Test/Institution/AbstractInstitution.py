# _*_ coding: utf-8 _*_
class AbstractInstitution:
    def __init__(self, belong: str, type: str):
        self.belong = belong
        self.type = type

    def load_file_content_for_date(self, file_name: str):
        return NotImplemented
