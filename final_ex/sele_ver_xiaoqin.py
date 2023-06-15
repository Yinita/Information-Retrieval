from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os
import chardet
import re



def extract_id(link):
    match = re.search(r'id=(\d+)', link)
    if match:
        return match.group(1)  # 返回第一个括号中匹配的部分
    else:
        return None



def login(driver, username, password):
    login_url = "https://www1.szu.edu.cn/board/infolist.asp?"  # 替换为登录页面的URL
    # 打开登录页面
    driver.get(login_url)
    # 输入用户名和密码
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    # 点击登录按钮
    login_button = driver.find_element(By.CSS_SELECTOR, ".auth_login_btn")
    login_button.click()
def init():
    # 登录并获取driver
    username = "xxxxxx"  # 需要提供真实可用的校园网账号密码
    password = "xxxxxx"

    # 设置WebDriver的路径
    driver_path = "..//chromedriver"  # 替换为ChromeDriver的路径
    driver = webdriver.Chrome(executable_path=driver_path)

    # login(driver, username, password)

    return driver

def main(driver, mode = "xqxw"):
    count = "1"
    link_dict = {}  # 创建一个空字典来保存 count 和对应的链接
    base_url = "https://xq40.szu.edu.cn/"
    # 执行搜索
    if mode == "xqxw":  # 三种网站， 一种是 base_url + xqdt/ + number/number.htm
        base_url += "xqdt/" # 一种是 各个学院的网页，我们可以仿照xqdt的处理 一种是 tx-news
        html_class = ["xqxw.htm"] + [f"xqxw//{i}.htm" for i in range(1, 12)]  # 1到11个页面
    elif mode == "tzgg":   # 都是各种通知公告,跟xqxw比较像
        html_class = ["tzgg.htm"] + [f"tzgg//{i}.htm" for i in range(1, 5)]  # 1到5个页面
    elif mode == "mtbd":  # 都是各种新闻网站
        base_url += "xqdt/"
        html_class = ["mtbd.htm"] + [f"mtbd//{i}.htm" for i in range(1, 7)]  # 1到7个页面


    # 获取搜索结果页面的HTML内容
    for html in html_class:
        url = base_url + html
        driver.get(url)
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        target_folder = f"data//{mode}"  # path
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        news_links = []
        for a in soup.find_all("a"):
            if 'href' in a.attrs:
                if a['href'].startswith('../info'):
                    news_links.append(base_url + a["href"])
                elif a['href'].startswith('https:'):
                    if a['href'] == "https://giving.szu.edu.cn/" or a['href'] == "https://www.szu.edu.cn":
                        continue
                    else:
                        news_links.append(a['href'])


        for index, link in enumerate(news_links):
            download_url = link
            if link.startswith("https://bs.szu.edu.cn/") or link.startswith("https://beian.miit.gov.cn/"):
                continue   # 无效
            print(link)
            driver.get(download_url)
            link_dict[count] = link
            file_name = os.path.join(target_folder, count + ".html")
            count = str(int(count) + 1)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"Downloaded {download_url} to {file_name}")
    # 将字典保存为一个 txt 文件
    with open(f"{mode}_msg.txt", 'w', encoding='utf-8') as f:
        for count, link in link_dict.items():
            f.write(f"{count} {mode} {link}\n")
    # 关闭浏览器
    driver.quit()


if __name__ == "__main__":
    #driver = init()
    #main(driver, "xqxw")
    #driver = init()
    #main(driver, "mtbd")
    #driver = init()
    #main(driver, "tzgg")
    """
    1.
    前缀为:  
    校庆新闻:
    xqxw.htm, xqxw//1.htm - xqxw//11.htm
    xpath:
    /html/body/div[4]/div/div[2]/ul/li[1]/a[1]
    对应的例子:
    <a href="../info/1015/1521.htm" class="flex L-Affiliate-Tagged" title="数字学术服务创新与发展研讨会暨CALIS第二十一届引进数据库培训周在深圳大学开幕">

                        
    媒体报道:
    mtbd.htm, mtbd//1.htm - mtbd//7.htm
    2.
    前缀为:  https://xq40.szu.edu.cn/
    通知公告:
    tzgg.htm, tzgg/5.htm - tzgg/1.htm
    
    """