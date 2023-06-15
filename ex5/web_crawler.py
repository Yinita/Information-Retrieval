import requests
from bs4 import BeautifulSoup
import os
import chardet
def download_html(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)

    else:
        print(f"Error: Unable to download {url} - {response.status_code}")



def login(username, password):
    login_url = "https://www1.szu.edu.cn/board/view.asp?id=487359"  # 替换为登录页面的URL
    session = requests.Session()

    # 发送登录请求
    data = {
        'username': username,
        'password': password,
    }
    response = session.post(login_url, data=data)

    if response.status_code == 200:
        print("Login successful!")
        session.cookies.update(response.cookies)
    else:
        print("Login failed!")
        session = None

    return session


def main():
    username = "413127"
    password = "12232315"
    session = login(username, password)

    if session:
        # 用获取到的session来请求其他需要登录才能访问的页面
        response = session.get("https://www.example.com/some_page")
        # 爬取数据的逻辑
    """
    base_url = "https://chat.openai.com/?model=gpt-4"  # 替换为您需要爬取的网站URL
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    """
    base_url = "https://www1.szu.edu.cn/board/"


    with open('list/1.html', 'rb') as f:
        raw_data = f.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
        html_content = raw_data.decode(detected_encoding)

    soup = BeautifulSoup(html_content, 'html.parser')

    target_folder = "downloaded_html"
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    news_links = []

    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) == 6:
            a_tag = tds[3].find("a")
            if a_tag is not None:
                news_links.append(a_tag["href"])
            else:
                print("Warning: Could not find an <a> tag in the specified <td>.")
    session = login(username, password)
    if session:
        # 用获取到的session来请求其他需要登录才能访问的页面
        for index, link in enumerate(news_links[:40]):
            download_url = link
            response = session.get(download_url)

            # 检查是否成功获取页面内容
            if response.status_code == 200:
                file_name = os.path.join(target_folder, f"news_{index + 1}.html")
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"Downloaded {download_url} to {file_name}")
            else:
                print(f"Error: Unable to download {download_url} - {response.status_code}")
    else:
        print("Login failed. Cannot download news pages.")

if __name__ == "__main__":
    main()
