from bs4 import BeautifulSoup
import os
import re


def extract_text_from_title_time_and_p(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    titles = [title.get_text() for title in soup.find_all('title')]
    paragraphs = [p.get_text() for p in soup.find_all('p')]

    # 提取初始化时间
    init_time_tag = soup.find('td', {'align': 'center', 'style': 'font-size: 9pt'})
    # print(init_time_tag)
    init_time = re.search(r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', init_time_tag.get_text())
    init_time = init_time.group() if init_time else ""

    # 提取编辑时间
    edit_time_tag = soup.find('td', text=re.compile('本文更新于'))
    edit_time = re.search(r'\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', edit_time_tag.get_text())
    edit_time = edit_time.group() if edit_time else ""

    all_texts = titles + paragraphs
    return [' '.join(all_texts), str(init_time), str(edit_time)]


# 这个函数接收一个文件路径（HTML 文件），提取文本，然后将结果保存到同一目录下的同名 TXT 文件和msg文件（记录信息）
def process_html_file(html_file_path):
    # 使用你的函数从 HTML 文件中提取文本
    extracted_text = extract_text_from_title_time_and_p(html_file_path)
    # 将 HTML 文件名替换为 TXT 文件名
    txt_file_path = html_file_path.replace('.html', '.txt')

    parts = html_file_path.split('\\')  # data\2021_党政办公室\464977.html
    number = parts[2].replace('.html', '')
    msg_txt_file_path = html_file_path.replace('\\' + parts[2], '_msg.txt')

    # 将提取的文本保存到 同名txt 文件
    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text[0])

    # 读取 msg.txt 文件
    with open(msg_txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 在内存中修改指定行
    for i, line in enumerate(lines):
        if line.startswith(number):
            lines[i] = line.strip() + " " + extracted_text[1] + " " + extracted_text[2] + '\n'

    # 将修改后的内容写回 msg.txt 文件
    with open(msg_txt_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"Processed {html_file_path} and saved to {txt_file_path}")



"""
    70年校庆模块

"""


def extract_all_chinese(html_file_path):
    # 读取 HTML 文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 使用 BeautifulSoup 来解析 HTML，然后提取所有文本
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.text

    # 使用正则表达式来提取所有中文字符
    chinese_text = re.findall(r'[\u4e00-\u9fa5]+', text)
    chinese_text_str = ''.join(chinese_text)
    return chinese_text_str

import re

def extract_text_and_time_xqxw(html_file_path, mode):
    # 读取 HTML 文件
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 尝试提取发文单位，如果没有找到，尝试使用备选的标签和属性
    link_text_element = soup.find('a', {'class': 'wx_tap_link js_wx_tap_highlight weui-wa-hotarea', 'id': 'js_name'})
    if link_text_element is None:
        link_text_element = soup.find('div', {'class': 'name b'})
    if link_text_element is None:
        link_text_element = soup.find('div', {'id': 'NewsArticleAuthor'})
    link_text = link_text_element.get_text(strip=True).split(' ')[0] if link_text_element is not None else ''
    link_text = link_text.replace("\n", "").replace(" ", "")  # 去除空格和换行

    # 尝试提取发布时间，如果没有找到，尝试使用备选的标签和属性
    publish_time_element = soup.find('em', {'id': 'publish_time', 'class': 'rich_media_meta rich_media_meta_text'})
    if publish_time_element is None:
        publish_time_element = soup.find('div', {'class': 'time c_999'})
    if publish_time_element is None:
        publish_time_element = soup.find('div', {'id': 'NewsArticlePubDay'})
    publish_time = publish_time_element.get_text(strip=True) if publish_time_element is not None else ''

    if mode == "mtbd":
        title_element = soup.find('h2', {'id': 'title', 'class': 'title'})
        if title_element is None:
            title_element = soup.title
    else:
        # 尝试提取标题，如果没有找到，尝试使用备选的标签和属性
        title_element = soup.find('h1', {'class': 'rich_media_title', 'id': 'activity-name'})
        if title_element is None:
            title_element = soup.title
        if title_element is None:
            title_element = soup.find('div', {'class': 'area-tit c_cca84d bb'})
        if title_element is None:
            title_element = soup.find('meta', {'charset': 'utf-8'})
        if title_element is None:   # 实在不行找h2
            title_element = soup.find('h2', {'id': 'title', 'class': 'title'})
    title = title_element.get_text(strip=True) if title_element is not None else ''
    title = title.replace("\n", "").replace(" ", "")  # 去除空格和换行
    title = re.sub(r'[^a-zA-Z\d\u4e00-\u9fa5]', '', title)  # 仅保留中文和英文字符和数字
    # print(link_text, publish_time, title)
    return link_text, publish_time, title



def process_html_file_xqxw(html_file_path):
    mode = os.path.basename(os.path.dirname(html_file_path))  # 取路径中倒数第二级的名称作为 mode
    #print(mode)
    # 使用你的函数从 HTML 文件中提取文本和时间
    link_text, publish_time, title = extract_text_and_time_xqxw(html_file_path, mode)
    # 将 HTML 文件名替换为 TXT 文件名
    txt_file_path = html_file_path.replace('.html', '.txt')
    parts = html_file_path.split('\\')  # data\2021_党政办公室\464977.html
    number = parts[2].replace('.html', '')
    msg_txt_file_path = html_file_path.replace('\\' + parts[2], '_msg.txt')
    content = extract_all_chinese(html_file_path)
    # 将提取的文本保存到同名txt 文件
    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 直接将number，发布时间，链接文本中的中文按顺序写入到 msg.txt 文件中
    with open(msg_txt_file_path, 'a', encoding='utf-8') as f:
        f.write(number + " " + " " + title + " " + publish_time + " " + link_text + '\n')

    print(f"Processed {html_file_path} and saved to {txt_file_path}")



def main(directory):  # data
    for root, dirs, files in os.walk(directory):
        # 遍历所有文件
        level = root.count(os.sep)
        if level == 1:
            # 遍历所有文件
            for file_name in files:
                if file_name.endswith(".html"):
                    # 获取完整文件路径
                    file_path = os.path.join(root, file_name)
                    # 对文件进行处理
                    print(file_path)
                    process_html_file_xqxw(file_path)   # process_html_file



if __name__ == "__main__":
    main("xq_70_data")
