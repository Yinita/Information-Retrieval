import streamlit as st
import main_pipeline
import xqxw_pipeline
PAGES = {
    "公文通": main_pipeline,
    "校庆新闻": xqxw_pipeline
}
st.sidebar.title('新闻来源')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
#  streamlit run .\main_page.py