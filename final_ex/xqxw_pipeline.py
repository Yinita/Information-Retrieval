import CN_simi_cal as sc
import invert_index as ii
import streamlit as st
import msg_match as mm
import time


# 加载停用词表
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)


def read_files(file_list, n=20):
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


# 校庆板块 !!!
def UI_xqxw(inverted_index, dir_prefixes):
    st.title("校庆新闻查询页面")
    query = st.text_input("请输入查询内容")
    classification_options = ['不限', '校庆新闻', '通知公告', '媒体报道']
    selected_classification = st.selectbox("请选择类别", classification_options)
    dict_classification_options = {'不限': "0", '校庆新闻': "1", '通知公告': "2", '媒体报道': "3"}
    selected_classification = dict_classification_options[selected_classification]
    # 创建一个按钮，在点击时调用搜索函数
    if st.button("搜索"):
        search_xqxw(query, selected_classification, inverted_index, dir_prefixes)


def search_xqxw(query, selected_classification, inverted_index, dir_prefixes):
    start_time = time.time()  # 记录开始时间
    file_list = []
    sorted_results = ii.pool_query_results(query, inverted_index)
    # 根据类别过滤信息
    info_list = mm.filter_by_class_xqxw(sorted_results, selected_classification)

    # 获取前20个结果的数字列表
    number_list = read_files(info_list, 20)
    # 为每个number查找并读取对应的文件，将结果添加到file_list中
    for number in number_list:
        # 在子文件夹中搜索原文件，来进行文本相似度计算
        key = next((key for key, val in dir_prefixes.items() if val == number[0]), None)
        path = f"xq_70_data/{key}/{number[1:]}.txt"
        result = sc.read_file_and_tokenize(path, mode=2)  # 偷懒 不写重构
        file_list.append(result)
    k = 10
    results = sc.rank_results(query, file_list, k)
    new_results = []
    # results的形状是[('128', 0.03108789591412647), ('141', 0.02733701995369217), ('129', 0.02630836526599162)]
    for result in results:
        new_results.append(mm.search_xqxw(result, dir_prefixes))
        # result[0], result[1], title, link, related_info, msg_cls

    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算经过的时间
    UIout_xqxw(new_results)
    # 例子 ['128', 0.03108789591412647, '法语文化爱好者有了深圳根据地深圳法语联盟在深圳大学揭牌',
    # 'https://appdetail.netwin.cn/web/2023/04/215aa6fdbdf1ac5fd7ff896fa6e0cdd9.html', '读创客户端']

    # 在页面的角落显示经过的时间
    st.sidebar.write(f"Search time: {elapsed_time:.2f} seconds")


def UIout_xqxw(results):  # title, link, related_info
    start_time = time.time()  # 记录开始时间
    # 如果没有找到结果，打印提示信息并返回
    if not results or results == [[]]:
        st.write("没有找到匹配的结果")
        return

    # 首先，处理并显示结果
    for result in results:
        msg_cls = "校庆新闻"
        if result[5] == "tzgg":
            msg_cls = "通知公告"
        elif result[5] == "mtbd":
            msg_cls = "媒体报道"
        display_text = f"##### [{result[2]}]({result[3]})  \n\n"  # 主标题
        display_text += f" - 相关度得分：{result[1]:.4f}\n"  # 小一号字体
        display_text += f" - 相关信息：{result[4]}\n"  # 小一号字体
        display_text += f" - 新闻板块：{msg_cls}\n"  # 小一号字体

        st.markdown(display_text)
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算经过的时间
    st.sidebar.write(f"imshow time: {elapsed_time:.2f} seconds")


def app():
    directory = "xq_70_data"
    dir_prefixes = {"mtbd": "1", "tzgg": "2", "xqxw": "3"}
    # 建立倒排索引
    inverted_index = build_inverted_index(directory)
    UI_xqxw(inverted_index, dir_prefixes)
    # 用法 streamlit run .\xqxw_pipeline.py


if __name__ == '__main__':
    app()
