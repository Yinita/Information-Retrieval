from bs4 import BeautifulSoup
import os
import re

def extract_text_from_title_and_p(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    titles = soup.find_all('title')
    paragraphs = soup.find_all('p')

    extracted_text = []
    for tag in titles + paragraphs:
        # 去除HTML格式符和超文本空格
        text = re.sub(r'<[^>]+>', '', tag.get_text())
        text = text.replace('&nbsp;', ' ')
        extracted_text.append(text.strip())

    return ' '.join(extracted_text)



def save_extracted_text_to_txt(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.html'):
            file_path = os.path.join(folder_path, file_name)
            result = extract_text_from_title_and_p(file_path)

            txt_file_name = file_name.replace('.html', '.txt')
            txt_file_path = os.path.join(folder_path, txt_file_name)

            with open(txt_file_path, 'w', encoding='utf-8') as f:
                f.write(result)

            print(f"Extracted text from {file_path} and saved to {txt_file_path}")


# 示例：处理所有文件夹中的HTML文件，并将结果保存到同名TXT文件中
folder_paths = ["D:\homework//2023 -1l\IR\ex5\党政办公室", "D:\homework//2023 -1l\IR\ex5\招生办公室",
                "D:\homework//2023 -1l\IR\ex5\教务处", "D:\homework//2023 -1l\IR\ex5\研究生院",
                "D:\homework//2023 -1l\IR\ex5\科学技术部"]

for folder_path in folder_paths:
    save_extracted_text_to_txt(folder_path)
