import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from wordcloud import WordCloud


def filter_articles(url, theme, field=None):
    param = {
        "searchType": "MulityTermsSearch",
        "ParamIsNullOrEmpty": "false",
        "Islegal": "false",
        "Theme": theme,
        "ExcludeField": field,
    }
    response = requests.post(FILTER_URL, param)
    res = {
        "name": [],
        "count": [],
        "code": [],
    }
    for e in response.json():
        name, count, code, _ = e.values()
        res["name"].append(name)
        res["count"].append(count)
        res["code"].append(code)
    return res


def wordcloud(df, word, count):
    word_freq = dict(zip(df[word], df[count]))
    wordcloud = WordCloud(
        font_path="SimHeiBold.ttf", width=1000, height=500, background_color="white"
    ).generate_from_frequencies(word_freq)
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")  # Hide axes
    return fig


FILTER_URL = "https://search.cnki.com.cn/api/fileterresultapi/articlefileter"

st.set_page_config(page_title="Trendio", layout="wide")
st.title("Trendio")
st.sidebar.header("Configuration")

years, types, subjects = st.tabs(["Years", "Types", "Subjects"])

if theme := st.sidebar.text_input("Theme", placeholder="Search something"):
    yrs = pd.DataFrame.from_dict(filter_articles(FILTER_URL, theme, field="Year"))
    years.line_chart(yrs, x="name", y="count", x_label="", y_label="")
    tps = pd.DataFrame.from_dict(filter_articles(FILTER_URL, theme, field="Type"))
    types.bar_chart(tps, x="name", y="count", x_label="", y_label="", horizontal=True)
    subjs = pd.DataFrame.from_dict(filter_articles(FILTER_URL, theme, field="Subject"))
    subjects.pyplot(wordcloud(subjs, "name", "count"))
