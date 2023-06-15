from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os
import chardet


def search(driver, year, unit):
    # 选择日期
    select_day = Select(driver.find_element(By.NAME, 'dayy'))
    select_day.select_by_value(year)  # 选择特定年份

    # 选择发文单位
    select_unit = Select(driver.find_element(By.NAME, 'from_username'))
    select_unit.select_by_value(unit)  # 选择特定单位

    # 点击搜索按钮
    search_button = driver.find_element(By.NAME, 'searchb1')
    search_button.click()

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

def main(year='2023', unit='党政办公室'):
    # 登录并获取driver
    username = "xxx"  # 需要提供真实可用的校园网账号密码
    password = "xxx"

    # 设置WebDriver的路径
    driver_path = "../chromedriver"  # 替换为ChromeDriver的路径
    driver = webdriver.Chrome(executable_path=driver_path)

    login(driver, username, password)
    # base_url = "https://www1.szu.edu.cn/board/infolist.asp?"
    base_url = "https://www1.szu.edu.cn/board/"
    # 执行搜索
    search(driver, year, unit)

    # 获取搜索结果页面的HTML内容
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    target_folder = year+"_"+unit  # path
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
    # 用获取到的driver来请求其他需要登录才能访问的页面
    for index, link in enumerate(news_links[:40]):
        download_url = base_url+link
        print(download_url)
        driver.get(download_url)

        # 检查是否成功获取页面内容
        if driver.current_url == download_url:
            file_name = os.path.join(target_folder, link[12:] + ".html")
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"Downloaded {download_url} to {file_name}")
        else:
            print(f"Error: Unable to download {download_url}")

    # 关闭浏览器
    driver.quit()


if __name__ == "__main__":
    main()