import os
import json


def initialize_index(directory='data'):
    index = {}
    for root, dirs, files in os.walk(directory):
        if root != directory:  # 如果不是在根目录级别
            year, department = os.path.basename(root).split('_')
            if year not in index:
                index[year] = {}
            if department not in index[year]:
                index[year][department] = []
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_id = file_name[:-4]  # remove .txt
                    index[year][department].append(file_id)

    # 将索引保存到 JSON 文件中
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False)

def load_index(file_path='index.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        index = json.load(f)
    return index

def find_file_path(doc_id, index):
    for year, departments in index.items():
        for department, doc_ids in departments.items():
            if str(doc_id) in doc_ids:
                return os.path.join('data', year + '_' + department, str(doc_id) + '.txt')
    return None


if __name__ == "__main__":
    index=load_index()
    doc_id=470428
    path=find_file_path(doc_id, index)
    print(path)
    if path == "data\\2023_党政办公室\\470428.txt":
        print("test good")
