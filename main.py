import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, html, dcc
import plotly.express as px
import altair as alt
from IPython.core.pylabtools import figsize


with st.echo(code_location='below'):
    """
    ## Hello, there you can find overview of mc'donalds nutrition !
    The data from https://raw.githubusercontent.com/Enjia/Nutrition-Facts-for-McDonald-s-Menu/master/menu.csv:
    """


    @st.cache
    def get_data():
        url = "https://raw.githubusercontent.com/Enjia/Nutrition-Facts-for-McDonald-s-Menu/master/menu.csv"
        df = pd.read_csv(url)
        df["Serving Size"] = df["Serving Size"].str.split().apply(pd.Series).iloc[:, 2].str[1:].sort_values()
        df = df[df["Serving Size"] != "oz"]
        df["Total Fat"] = df["Total Fat"].astype('int32')
        smry = df[["Item", 'Calories', 'Total Fat',
                   'Total Fat (% Daily Value)', 'Carbohydrates',
                   'Carbohydrates (% Daily Value)', "Protein", "Category"]]
        return smry

# how many items have more than 200 calories
    smry = get_data()

    st.write(smry.sample(frac=1))


    def print_hello(name="World"):
        st.write(f"### Hello, {name}!")


    name = st.text_input("Your name", key="name", value="Anonymous")
    print_hello(name)

    """"
    # First chart
    """

    item = st.selectbox("Item", smry["Item"])
    st.write(item)
    c = smry[smry.Item == item].index[0]
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize= (6, 4))
    # fig.patch.set_facecolor('xkcd:mint green')
    plt.title(smry.Item[c] + " (" + str(smry.Calories[c]) + "calories" + " )")
    plt.bar(x=smry.iloc[c, [2, 4, 6]].index, height=smry.iloc[c, [2, 4, 6]])
    # plt.ylim((50, None))
    bottom, top = plt.ylim()
    plt.ylim((bottom, top+10))
    for index, value in enumerate(smry.iloc[c, [2, 4, 6]]):
        plt.text(index - 0.05, value + 0.5, str(value))
    st.pyplot(fig)


    """"
    
    # Second chart
    
    """

    sns.set_theme()
    sns.set_style("dark")
    plt.style.use("dark_background")

    cat = st.selectbox("Category", smry["Category"].unique())
    # cat = "Snacks & Sides"
    var = "Calories"
    # dct = {"Calories" : 2500 , ...}
    standart = 2500
    sns.color_palette("mako", as_cmap=True)

    brkf = smry[smry.Category == cat].sort_values(var)
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(x="Item", y="Calories", data=brkf)

    plt.axhline(y=standart // 2, color='r', linestyle='-', label=f"a half of standart {var.lower()} consumption")
    plt.legend()
    plt.grid(linestyle='-', linewidth=0.1)
    ax.set(xticklabels=[])
    st.pyplot(fig)

    """"

    # Second chart

    """
    fig = px.bar(smry[smry.Category == cat].sort_values(var), x="Item", y=var)
    st.plotly_chart(fig)

