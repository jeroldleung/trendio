import asyncio

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
        self.Order: str = None

    def set_params(self, theme=None, exclude_field=None, order=None):
        if theme:
            self.theme = theme
        if exclude_field:
            self.ExcludeField = exclude_field
        if order:
            self.Order = order

    async def fetch(self):
        response = requests.post(self.url, data=self.__dict__).json()
        return response


def wordcloud(text):
    wordcloud = WordCloud(
        font_path="SimHeiBold.ttf", width=1000, height=500, background_color="white"
    ).generate(text)
    fig = plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")  # Hide axes
    return fig


st.set_page_config(page_title="Trendio", layout="wide")
st.title("Trendio")

theme = st.text_input(
    "Theme",
    value="Artificial Intelligence",
    placeholder="Search Something",
    label_visibility="collapsed",
)

article_filter = CnkiService("https://search.cnki.com.cn/api/fileterresultapi/articlefileter")
article_filter.set_params(theme=theme)

paper_list = CnkiService("https://search.cnki.com.cn/api/search/listresult")
paper_list.set_params(theme=theme)

wordcloud_col, year_col = st.columns([2, 1])

# get and plot the wordcloud of keywords of most downloaded articles
paper_list.set_params(order="3")
papers = pd.DataFrame.from_dict(asyncio.run(paper_list.fetch())["articleList"])
key_word = "".join(papers["keyWord"])
wordcloud_col.pyplot(wordcloud(key_word))

# get and plot the number of articles of each years
article_filter.set_params(exclude_field="Year")
years = pd.DataFrame.from_dict(asyncio.run(article_filter.fetch()))
fig = px.line(years, x="FilterName", y="ArticleCount")
fig.update_layout(title_text="Academic Research Index Analysis", yaxis_title=None, xaxis_title=None)
year_col.plotly_chart(fig, use_container_width=True)

# table of articles
fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[400, 80],
            header=dict(values=["Title", "Downloads"]),
            cells=dict(values=[papers.title, papers.downloadCount]),
        )
    ]
)
fig.update_layout(title_text="Table of Articles")
st.plotly_chart(fig, use_container_width=True)

type_col, subject_col, level_col = st.columns(3)

# get and plot the number of articles of each types
article_filter.set_params(exclude_field="Type")
types = pd.DataFrame.from_dict(asyncio.run(article_filter.fetch()))
fig = px.bar(types, x="FilterName", y="ArticleCount")
fig.update_layout(title_text="Article Type", yaxis_title=None, xaxis_title=None)
type_col.plotly_chart(fig, use_container_width=True)

# get and plot the number of articles of each subjects
article_filter.set_params(exclude_field="Subject")
subjects = pd.DataFrame.from_dict(asyncio.run(article_filter.fetch()))
fig = px.bar(subjects, x="ArticleCount", y="FilterName", orientation="h")
fig.update_layout(title_text="Subject Classification", yaxis_title=None, xaxis_title=None)
subject_col.plotly_chart(fig, use_container_width=True)

# get and plot the number of articles of each levels
article_filter.set_params(exclude_field="Level")
levels = pd.DataFrame.from_dict(asyncio.run(article_filter.fetch()))
fig = px.bar(levels, x="ArticleCount", y="FilterName", orientation="h")
fig.update_layout(title_text="Research Level Distribution", yaxis_title=None, xaxis_title=None)
level_col.plotly_chart(fig, use_container_width=True)
