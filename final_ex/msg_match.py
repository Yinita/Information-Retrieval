import os
import glob
from datetime import datetime, timedelta
import json

def convert_msg_to_dict(msg_txt_file_path, json_file_path):
    with open(msg_txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 将每一行的内容转换为字典的键值对
    msg_dict = {}
    for line in lines:
        components = line.strip().split(' ')
        number = int(components[0])
        classification = components[1]
        time1 = components[2] + ' ' + components[3]
        time2 = components[4] + ' ' + components[5]
        msg_dict[number] = [classification, time1, time2]

    # 将字典保存为 json 文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(msg_dict, f, ensure_ascii=False)


def load_msg_dict(json_file_path):
    # 从 json 文件加载字典
    with open(json_file_path, 'r', encoding='utf-8') as f:
        msg_dict = json.load(f)
    return msg_dict

def find_in_msg_dict(msg_dict, target_number):
    # 从字典中查找信息
    if str(target_number) in msg_dict:
        return [target_number] + msg_dict[str(target_number)]
    return None

def get_info_for_numbers(number_list, msg_dict):
    # 从字典中获取信息
    info_list = []
    for number in number_list:
        info = find_in_msg_dict(msg_dict, number[0])
        if info is not None:
            info_list.append(info)
    return info_list


def filter_by_class(info_list, class_name):
    # 同类返回
    if class_name == "不限":
        return info_list
    else:
        filtered_list = [info for info in info_list if info[1] == class_name]
    return filtered_list


def filter_by_time(info_list, time_option):
    if time_option == "不限":
        return info_list
    else:
        now = datetime.now()
        if time_option == "30天内":
            time_limit = now - timedelta(days=30)
        elif time_option == "半年内":
            time_limit = now - timedelta(days=180)
        elif time_option == "一年内":
            time_limit = now - timedelta(days=365)

        filtered_list = []
        for info in info_list:
            time2 = datetime.strptime(info[3], "%Y/%m/%d %H:%M:%S")
            if time2 >= time_limit:
                filtered_list.append(info)
        return filtered_list


def filter_by_class_xqxw(sorted_results, state):
    # 同类返回
    if state == "0":   # 解释一下，0代表不限，1,2,3分别是三种类别作为前缀出现
        return sorted_results
    else:
        filtered_list = [result for result in sorted_results if str(result[0])[0] == state]
    return filtered_list


def search_xqxw(result, dir_prefixes):
    # print(result)
    # print(dir_prefixes)
    key = next((key for key, val in dir_prefixes.items() if val == result[0][0]), None)
    if key is not None:
        file_name = f"xq_70_data/{key}_msg.txt"
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith(result[0][1:]):
                _, title, *related_info = line.split(' ')
                title = title.split('\n')[0]   # 补丁 避免异常显示
                if related_info:
                    related_info[-1] = related_info[-1][:-1]
                    related_info = ' '.join(related_info)  # -1是防止 \n
                else:
                    related_info = ""
                continue

        file_name = f"xq_70_data/{key}_link.txt"
        with open(file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(result[0][1:]):
                    split_line = line.split(' ')
                    msg_cls = split_line[1]
                    link = split_line[2][:-1]  # -1是防止 \n
                    return [result[0], result[1], title, link, related_info, msg_cls]
    return None

def sort_and_save_all_msg(dir_path):
    # 搜索文件夹内所有的 .msg.txt 文件
    files = glob.glob(os.path.join(dir_path, '*_msg.txt'))

    # 存储所有的信息
    all_info = []

    # 对于每个文件，使用 get_info_for_numbers 函数获取所有的信息
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            # print(file)
            lines = f.readlines()
            for line in lines:
                components = line.strip().split(' ')
                number = components[0]
                classification = components[1]
                time1 = components[2] + ' ' + components[3]
                time2 = components[4] + ' ' + components[5]
                all_info.append([number, classification, time1, time2])

    # 根据 number 排序所有的信息
    all_info.sort(key=lambda x: x[0])

    # 保存到 map_all_msg.txt
    with open(os.path.join(dir_path, 'map_all_msg.txt'), 'w', encoding='utf-8') as f:
        for info in all_info:
            f.write(' '.join(info) + '\n')


#convert_msg_to_dict("data/map_all_msg.txt", "data/map_all.json")
#sort_and_save_all_msg('data')
#print(find_in_msg_file("data/2022_学报理工版_msg.txt", 481045))