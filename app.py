import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from wordcloud import WordCloud


class CnkiService:
    def __init__(self, request_url):
        self.url = request_url
        self.searchType = "MulityTermsSearch"
        self.ParamIsNullOrEmpty = "false"
        self.Islegal = "false"
        self.Theme: str = None
        self.ExcludeField: str = None

    def set_params(self, theme=None, exclude_field=None):
        if theme:
            self.theme = theme
        if exclude_field:
            self.ExcludeField = exclude_field

    def fetch(self):
        response = requests.post(self.url, data=self.__dict__)
        return response.json()


def wordcloud(df, word, count):
    word_freq = dict(zip(df[word], df[count]))
    wordcloud = WordCloud(
        font_path="SimHeiBold.ttf", width=1000, height=500, background_color="white"
    ).generate_from_frequencies(word_freq)
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")  # Hide axes
    return fig


st.set_page_config(page_title="Trendio", layout="wide")
st.title("Trendio")

theme = st.text_input("Theme", placeholder="Search Something", label_visibility="collapsed")

article_filter = CnkiService("https://search.cnki.com.cn/api/fileterresultapi/articlefileter")
article_filter.set_params(theme=theme)

# get and plot the number of articles of each years
article_filter.set_params(exclude_field="Year")
years = pd.DataFrame.from_dict(article_filter.fetch())
fig = px.line(years, x="FilterName", y="ArticleCount")
fig.update_layout(title_text="Academic Research Index Analysis", yaxis_title=None, xaxis_title=None)
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

# get and plot the number of articles of each subjects
article_filter.set_params(exclude_field="Subject")
subjects = pd.DataFrame.from_dict(article_filter.fetch())
fig = px.bar(subjects, x="ArticleCount", y="FilterName", orientation="h")
fig.update_layout(title_text="Subject Classification", yaxis_title=None, xaxis_title=None)
col1.plotly_chart(fig, use_container_width=True)

# get and plot the number of articles of each types
article_filter.set_params(exclude_field="Type")
types = pd.DataFrame.from_dict(article_filter.fetch())
fig = px.bar(types, x="FilterName", y="ArticleCount")
fig.update_layout(title_text="Article Type", yaxis_title=None, xaxis_title=None)
col2.plotly_chart(fig, use_container_width=True)

# get and plot the number of articles of each levels
article_filter.set_params(exclude_field="Level")
levels = pd.DataFrame.from_dict(article_filter.fetch())
fig = px.bar(levels, x="ArticleCount", y="FilterName", orientation="h")
fig.update_layout(title_text="Research Level Distribution", yaxis_title=None, xaxis_title=None)
col3.plotly_chart(fig, use_container_width=True)
