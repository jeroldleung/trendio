import requests
import streamlit as st

filter_url = "https://search.cnki.com.cn/api/fileterresultapi/articlefileter"
result_url = "https://search.cnki.com.cn/api/search/listresult"

st.set_page_config(layout="wide")

theme = st.sidebar.text_input("Theme", label_visibility="collapsed")

hot1, hot2, hot3, hot4, hot5 = st.columns(5)
hot1.write("")
hot2.metric("热词一", "70#", "1#")
hot3.metric("热词二", "70$", "-2$")
hot4.metric("热词三", "70%", "3%")
hot5.write("")


def fetch_data(url, theme, field=None, page=None, order=None):
    param = {
        "searchType": "MulityTermsSearch",
        "ParamIsNullOrEmpty": "false",
        "Islegal": "false",
        "Theme": theme,
        "ExcludeField": field,
        "Page": page,
        "Order": order,
    }
    return requests.post(url, data=param).json()


def extract_data(raw_data, x_label=None, y_label=None, key=None):
    res = {}
    if type(raw_data) == dict:
        raw_data = raw_data[key]
    for item in raw_data:
        res[item[x_label]] = item[y_label]
    return res


if st.sidebar.button("Search", type="primary", use_container_width=True):
    paper_type = extract_data(
        fetch_data(filter_url, theme, field="Type"),
        x_label="FilterName",
        y_label="ArticleCount",
    )
    paper_year = extract_data(
        fetch_data(filter_url, theme, field="Year"),
        x_label="FilterName",
        y_label="ArticleCount",
    )
    paper_subject = extract_data(
        fetch_data(filter_url, theme, field="Subject"),
        x_label="FilterName",
        y_label="ArticleCount",
    )
    paper_level = extract_data(
        fetch_data(filter_url, theme, field="Level"),
        x_label="FilterName",
        y_label="ArticleCount",
    )
    paper_list = extract_data(
        fetch_data(result_url, theme, order=3),
        x_label="title",
        y_label="downloadCount",
        key="articleList",
    )

    # plot the result paper type
    with st.container():
        st.subheader("文献类型")
        st.bar_chart(paper_type, horizontal=True)

    # plot the result paper year
    with st.container():
        st.subheader("学术研究指数分析")
        st.line_chart(paper_year)

    # plot the result paper subject and level
    subject_col, level_col = st.columns(2)
    with subject_col:
        st.subheader("学科分类")
        st.bar_chart(paper_subject, horizontal=True)
    with level_col:
        st.subheader("研究层次分布")
        st.bar_chart(paper_level, horizontal=True)

    # plot the most downloaded paper
    with st.container():
        st.subheader("相关论文下载趋势")
        st.table(paper_list)
