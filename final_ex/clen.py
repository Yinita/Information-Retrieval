import re
# 代码在多次运行时候会加入额外的空格，这个函数可以去除额外的空格


def remove_extra_whitespace(text):
    return re.sub(' +', ' ', text)

file_names = ["mtbd_msg.txt", "tzgg_msg.txt", "xqxw_msg.txt"]

for file_name in file_names:
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = [remove_extra_whitespace(line) for line in lines]

    with open(file_name, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
