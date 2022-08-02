# _*_ coding: utf-8 _*_
import email
import os
import sys

# msg_data = message_from_string(data.decode(msg_str, 'ignore'))
# 获取eml附件信息
from email.message import Message
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
import re


def decode_email_str(s: str):
    if s is None:
        return None
    elif s.startswith('=?'):
        decoded_list = decode_header(s)
        assert len(decoded_list) == 1, str(decoded_list)
        value, charset = decoded_list[0]
        if charset is not None:
            value = value.decode(charset)
        return value
    else:
        return s


def parse_tencent_email_content_part(msg_part: Message):
    result_list = list()
    if msg_part.is_multipart():  # 如果邮件对象是一个MIMEMultipart, 内容带附件
        for sub_msg_part in msg_part.get_payload():
            assert isinstance(sub_msg_part, Message), '{} {}'.format(type(sub_msg_part), sub_msg_part)
            result_list.extend(parse_tencent_email_content_part(sub_msg_part))
    else:

        new_part_obj = dict()
        new_part_obj['content_type'] = msg_part.get_content_type()
        content_main_type, content_sub_type = new_part_obj['content_type'].split('/')
        content_disposition = msg_part.get_content_disposition()
        new_part_obj['content_disposition'] = content_disposition
        new_part_obj['charset'] = msg_part.get_content_charset()
        if content_disposition is None:  # 非附件
            if content_main_type == 'text':  # 处理文本内容
                try:
                    new_part_obj['data'] = msg_part.get_payload(decode=True).strip().decode(new_part_obj['charset'])
                except TypeError:
                    new_part_obj['data'] = ''
                except UnicodeDecodeError:
                    new_part_obj['data'] = ''
            elif content_main_type == 'image':
                new_part_obj['data'] = msg_part.get_payload(decode=True)
            elif content_main_type == 'application':
                try:
                    new_part_obj['name'] = decode_email_str(msg_part.get_filename()).replace('\r', '').replace('\n', '')
                except AttributeError:
                    from datetime import datetime
                    new_part_obj['name'] = 'unknown{}'.format(datetime.now())
                new_part_obj['data'] = msg_part.get_payload(decode=True)
            else:
                raise NotImplementedError('{}\n{}'.format(content_main_type, msg_part.as_string()))

        elif content_disposition == 'attachment':
            new_part_obj['name'] = decode_email_str(msg_part.get_filename()).replace('\r', '').replace('\n', '')
            assert new_part_obj['name'] is not None, msg_part.as_string()
            if content_main_type == 'application':  # 处理附件
                new_part_obj['data'] = msg_part.get_payload(decode=True)
            elif content_main_type == 'text':
                new_part_obj['data'] = msg_part.get_payload(decode=True)
            elif content_main_type == 'image':
                new_part_obj['data'] = msg_part.get_payload(decode=True)
            elif content_main_type == 'content':
                new_part_obj['data'] = msg_part.get_payload(decode=True)
            else:
                raise NotImplementedError('{} {}\n{}'.format(
                    content_disposition, content_main_type, msg_part.as_string()
                ))
            # o = open(r'C:\Users\Administrator.SC-201606081350\Downloads\test\{}'.format(new_part_obj['name']), 'wb')
            # o.write(new_part_obj['data'])
            # o.close()

        elif content_disposition == 'inline':

            if content_main_type == 'text':  # 处理文本内容
                new_part_obj['charset'] = msg_part.get_content_charset()
                try:
                    new_part_obj['data'] = msg_part.get_payload(decode=True).strip().decode(new_part_obj['charset'])
                except TypeError:
                    new_part_obj['data'] = ''
            elif content_main_type == 'application':
                pass
            elif content_main_type == 'image':
                pass
            else:
                raise NotImplementedError('{}\n{}'.format(content_main_type, msg_part.as_string()))

        else:
            raise NotImplementedError('{}\n{}'.format(content_disposition, msg_part.as_string()))
        result_list.append(new_part_obj)
    return result_list


def put_mail_cache(folder_name: str, uid: int, file_name: str, cache_bit: bytes):
    # folder_name = folder_name.replace('/', '$$$')
    os.makedirs(os.path.join(folder_name, str(uid)), exist_ok=True)
    file_name = file_name.replace('\t', '').replace('\\', '').replace(':', '').replace('/', '')
    bit_out = open(os.path.join(folder_name, str(uid), file_name), 'wb')
    bit_out.write(cache_bit)
    bit_out.close()


def __put_mail_text__(folder_name: str, mail_index: int, text: str, encoding='gb18030'):
    # folder_name = folder_name.replace('/', '$$$')
    os.makedirs(os.path.join(folder_name, str(mail_index)), exist_ok=True)
    if os.path.exists(os.path.join(folder_name, str(mail_index), '__main__.txt')):
        text_out = open(os.path.join(folder_name, str(mail_index), '__main__.txt'), 'a', encoding=encoding)
        try:
            text_out.write(text)
        except UnicodeEncodeError as u_error:
            print(text)
            raise u_error
        except TypeError:
            if isinstance(text, bytes):
                text_out.write(text.decode(encoding='gb18030', errors='ignore'))
            else:
                raise TypeError(' write() argument must be str, not {}'.format(type(text)))
        text_out.close()
    else:
        text_out = open(os.path.join(folder_name, str(mail_index), '__main__.txt'), 'w', encoding=encoding)
        try:
            text_out.write(text)
        except UnicodeEncodeError as u_error:
            print(text)
            raise u_error
        text_out.close()


def Get_Annex_Message(FilePath, Annex_Path, count):
    global sum
    fp = open(FilePath, 'rb')  # 打开任意格式文件，通过email库来判断是否为eml文件
    data = fp.read()
    msg_data = email.message_from_bytes(data)
    assert isinstance(msg_data, Message), str(msg_data)
    msg_str = msg_data.get_charset()
    if msg_str is None:
        try:
            charset_list = re.findall(re.compile('charset=(.*)\n'), msg_data.as_string())
            if len(charset_list) >= 1:
                msg_str = charset_list[0]
            else:
                charset_list = re.findall(re.compile('=\?(\w*)\?'), msg_data.as_string())
                if len(charset_list) >= 1:
                    msg_str = charset_list[0]
                else:
                    msg_str = None
                    for encoding_tag in ('gb18030', 'utf-8', 'gb2312', 'GBK'):
                        try:
                            data.decode(encoding=encoding_tag)
                            msg_str = encoding_tag
                        except UnicodeDecodeError:
                            continue
                    assert msg_str is not None, '未能识别邮件内容编码\n{}'.format(msg_data.as_string())
            try:
                # date.decode(encoding=mmsg_str)
                msg_data = email.message_from_string(data.decode(msg_str, 'ignore'))
                print(msg_data)
            except:
                print("unorder")
                return {"flag": "unorder"}
        except Exception as e:
            print(e)
    new_obj = dict()
    new_obj['charset'] = msg_str
    assert isinstance(msg_data, Message), str(msg_data)

    msg_str = msg_data.get('Message-Id')  # 获取邮件编号
    try:
        new_obj['message_id'] = msg_str.strip('<>')
    except AttributeError:
        new_obj['message_id'] = None

    msg_str = msg_data.get('Mime-Version')
    new_obj['mime_version'] = decode_email_str(msg_str)

    msg_str = msg_data.get('From')  # 获取发件人详情
    new_obj['from_nickname'], new_obj['from_account'] = parseaddr(msg_str)
    try:
        new_obj['from_nickname'] = decode_email_str(new_obj['from_nickname'])
    except UnicodeDecodeError:
        pass

    msg_str = msg_data.get('To')  # 获取收件人详情
    new_obj['to_nickname'], new_obj['to_account'] = parseaddr(msg_str)
    new_obj['to_nickname'] = decode_email_str(new_obj['to_nickname'])

    msg_str = msg_data.get('Subject')  # 获取主题信息
    new_obj['subject'] = decode_email_str(msg_str)

    msg_str = msg_data.get("Date")  # 获取时间信息
    new_obj['received_time'] = parsedate_to_datetime(msg_str)

    # print(new_obj)

    new_obj['content'] = parse_tencent_email_content_part(msg_data)
    try:
        for obj_dict in new_obj['content']:

            assert isinstance(obj_dict, dict)
            if obj_dict['content_disposition'] == 'attachment':
                # 储存附件
                if obj_dict['name'] is None:
                    obj_dict['name'] = 'None'
                elif len(obj_dict['name'].replace(' ', '')) == 0:
                    obj_dict['name'] = 'NoName'
                else:
                    pass
                put_mail_cache(Annex_Path, count, obj_dict['name'], obj_dict['data'])
            elif obj_dict['content_disposition'] in (None, 'inline'):
                if obj_dict.get('data', None) is None:
                    pass
                elif obj_dict.get('content_type', '').startswith('image'):
                    pass
                else:
                    if len(obj_dict.get('data', '')) > 0:
                        try:
                            __put_mail_text__(Annex_Path, count, obj_dict['data'])
                        except TypeError:
                            pass
                    else:
                        pass
            else:
                raise NotImplementedError('{}'.format(obj_dict))
        # self.db.add(mail_detail)  # 前面没在detail数据库表里查出来，现在把它加进去
    except Exception as e:
        print(e)

    return new_obj
    # msg = email.message_from_binary_file(data.decode(msg_data,'ignore'))
    # for part in msg.walk():  # 循环信件中的每一个mime的数据块
    #     if part.get_content_maintype() == 'multipart':
    #         continue
    #     Annex_name = part.get_filename()
    #     if Annex_name:  # 如果附件存在名字
    #         Annex_name = str(sum) + '.' + Annex_name
    #         fp = open(os.path.join(Annex_Path, Annex_name), 'wb','ignore')
    #         fp.write(part.get_payload(decode=True))
    #         sum += 1


# 递归文件夹下所有文件
count = 0


def List_Filepath(Eml_Path, Annex_Path):
    global count
    for parent, dirnames, filenames in os.walk(Eml_Path):  # 遍历文件夹
        for dirname in dirnames:  # 对文件夹进行递归
            count += 1
            List_Filepath(dirname, Annex_Path)

        for filename in filenames:  # r对文件进行判断
            FilePath = os.path.join(parent, filename)
            res = FilePath.split(os.path.sep)[-2]
            Get_Annex_Message(FilePath, Annex_Path, res)


# 创建目的文件夹
def Create_Dir(Annex_Path):
    if os.path.exists(Annex_Path):
        print("dir exists, Annex file will create in %s" % Annex_Path)
    else:
        os.mkdir(Annex_Path)


# 主函数
def main():
    global sum
    sum = int(1)
    Eml_Path = r'D:\Users\Desktop\mails\Temp'  # 第一个参数为eml所在文件夹
    Annex_Path = r'D:\Users\Desktop\mails\target'  # 第二个参数为eml附件输出的路径
    Create_Dir(Annex_Path)  # 创建保存附加的文件夹
    List_Filepath(Eml_Path, Annex_Path)


if __name__ == "__main__":
    main()
