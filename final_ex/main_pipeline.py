import file_index_generate as fig
import CN_simi_cal as sc
import invert_index as ii
import sele_ver as sv
import clean_data as cd
import extract_doc as ed
import streamlit as st
import msg_match as mm
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import time
import cProfile  # 分析性能
import pstats
# 加载停用词表
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)


def read_files(file_list, n = 20):
    file_ids = []
    for file_tuple in file_list:
        file_id = str(file_tuple[0])
        file_ids.append(file_id)
    return file_ids[:n]

# https://docs.streamlit.io/library/advanced-features/caching
#   cache_data ; cache_resource


@st.cache_data()
def build_inverted_index(directory):
    # 建立倒排索引
    tokenized_texts = ii.read_and_tokenize_files(directory)
    # token_count, term_count = ii.count_tokens_and_terms(tokenized_texts)  # 统计token和term总数
    inverted_index = ii.build_inverted_index(tokenized_texts)  # 构建倒排索引
    return inverted_index


# 公文通板块 !!!


def UIin(inverted_index, index, msg_dict):
    st.title("公文通查询页面")
    # 输入查询
    query = st.text_input("请输入查询内容")
    # 选择类别
    classification_options = ['不限', '讲座', '教务', '科研', '行政', '会议', '学工', '生活']
    selected_classification = st.selectbox("请选择类别", classification_options)
    # 选择时间范围
    time_options = ['不限', '30天内', '半年内', '一年内']
    selected_time = st.selectbox("请选择时间范围", time_options)
    # 添加一个滑动条来控制alpha的值
    alpha = st.slider("调整搜索结果的优先级（左边是标题优先，右边是内容优先）", min_value=0.0, max_value=1.0, value=0.5)
    # 创建一个按钮
    if st.button("搜索"):
        search(query, selected_classification, selected_time, inverted_index, index, msg_dict, alpha)



def search(query, selected_classification, selected_time, inverted_index, index, msg_dict, alpha=0.5):
    start_time = time.time()  # 记录开始时间
    file_list = []
    sorted_results = ii.pool_query_results(query, inverted_index)
    # 获取这些 number 对应的完整信息
    info_list = mm.get_info_for_numbers(sorted_results, msg_dict)
    # 根据类别过滤信息
    info_list = mm.filter_by_class(info_list, selected_classification)
    # 根据时间过滤信息
    info_list = mm.filter_by_time(info_list, selected_time)
    # 获取前n个结果的数字列表
    number_list = read_files(info_list, 40)
    # 为每个number查找并读取对应的文件，将结果添加到file_list中
    for number in number_list:
        path = fig.find_file_path(number, index)  # 在子文件夹中搜索原文件，来进行文本相似度计算
        if path is not None:  # 检查路径是否为 None
            result = sc.read_file_and_tokenize(path, title=1)  # id,content,title
            file_list.append(result)
    k = 10
    results = sc.rank_results_with_weights(query, file_list, k, alpha)
    new_results = []
    # print(results)
    for result in results:
        path = fig.find_file_path(result[0], index)
        with open(os.path.join(path), "r", encoding="utf-8") as file:
            content = file.read()
            content_until_dash = content.split("—", 1)[0]
            # 小的优化， 我们传入1作为参数，表示在搜到标题后就停止搜索
            _, classname, _ = path.split("\\")
            for info in info_list:
                if str(info[0]) == result[0]:
                    # 找到匹配的信息，将其添加到 new_result 中
                    new_result = (result[0], result[1], content_until_dash, classname, info[1], info[2], info[3])
                    new_results.append(new_result)
                    continue  # 找到信息后就退出循环

    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算经过的时间
    UIout(new_results)
    # 在页面的角落显示经过的时间
    st.sidebar.write(f"Search time: {elapsed_time:.2f} seconds")



def UIout(results):
    start_time = time.time()  # 记录开始时间
    # 如果没有找到结果，打印提示信息并返回
    if not results or results == [[]]:
        st.write("没有找到匹配的结果")
        return

    # 首先，处理并显示结果
    for result in results:
        url = f'https://www1.szu.edu.cn/board/view.asp?id={result[0]}'
        display_text = f"##### [{result[2]}]({url})  \n\n"  # 主标题
        display_text += f" - 相关度得分：{result[1]:.4f}\n"  # 小一号字体
        display_text += f" - 类别：{result[4]}\n"  # 类别为行政
        display_text += f" - 初始时间：{result[5]}\n"  # 初始时间
        display_text += f" - 修改时间：{result[6]}\n"  # 修改时间
        st.markdown(display_text)

    # 创建DataFrame，以便于统计类别数据
    df = pd.DataFrame(results, columns=['id', 'score', 'title', 'category', 'classification', 'time1', 'time2'])
    # 为 matplotlib 设置中文字体
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # 将类别列分割为两部分：年份和发文单位
    df[['year', 'unit']] = df['category'].str.split('_', expand=True)

    # 生成饼图
    for column in ['year', 'unit']:
        fig, ax = plt.subplots()
        df[column].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        plt.title(f'Category by {column.title()}')
        st.sidebar.pyplot(fig)
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算经过的时间
    st.sidebar.write(f"imshow time: {elapsed_time:.2f} seconds")


# 下载板块 !!!
def sele_ver():
    years = ["2023", "2022","2021, 2020, 2019, 2018", "2017"]  # "2023", "2022","2021, 2020, 2019, 2018 "
    '''
    
    '''
    units = ["校友联络部", "校团委","教务部", "附属教育集团", "深大附属中学", "深大附属实验中学", "中国经济特区研究中心","港澳基本法研究中心",
             "文化产业研究院", "美学与文艺批评研究院", "饶宗颐文化研究院", "党政办公室", "组织部", "统战部", "宣传部", "纪检（监察）室",
             "校工会", "妇女委员会", "离退休办公室","招生办公室", "创新创业教育中心", "研究生院", "党委研工部", "发展规划部", "社会科学部",
             "学报社科版", "科学技术部", "实验室与国有资产管理部", "审计室", "后勤保障部", "后勤保障部党委", "安全保卫部", "教育发展基金会",
             "学报理工版", "学生部", "党委学工部", "国际交流与合作部", "人力资源部", "党委教师工作部", "计划财务部", "招投标管理中心",
             "机关党委", "丽湖校区管理办公室", "教育学部", "艺术学部", "医学部", "马克思主义学院", "经济学院", "法学院", "心理学院", "体育学院",
             "人文学院", "外国语学院", "传播学院", "数学与统计学院", "物理与光电工程学院", "化学与环境工程学院", "生命与海洋科学学院", "机电与控制工程学院",
             "材料学院", "电子与信息工程学院", "计算机与软件学院", "建筑与城市规划学院", "土木与交通工程学院", "管理学院", "政府管理学院", "高等研究院",
             "金融科技学院", "国际交流学院", "继续教育学院", "图书馆", "图书馆党总支", "档案馆", "信息中心", "信息中心党总支", "资产经营公司",
             "技术转化中心", "深大总医院", "深大附属华南医院", "校医院", "中国海外利益研究院", "微纳光电子学研究院", "创新技术研究院",
             "大数据系统计算技术国家工程实验室", "心理健康教育与咨询中心",
             "人工智能与数字经济广东省实验室（深圳）", "深圳香蜜湖国际金融科技研究院", "人工智能与数字经济广东省实验室（深圳）"]
    for year in years:
        for unit in units:
            driver = sv.init()
            sv.main(driver, year, unit)
    ed.main()
    cd.process_files()



def app():
    directory = "data"
    msg_dict = mm.load_msg_dict(f"{directory}/map_all.json")
    file_list = []
    index = fig.load_index()
    # 建立倒排索引
    inverted_index = build_inverted_index(directory)
    UIin(inverted_index, index, msg_dict)
    # 用法 streamlit run .\main_pipeline.py

if __name__ == '__main__':
    #sele_ver()
    #fig.initialize_index()
    #mm.sort_and_save_all_msg("data")
    app()

