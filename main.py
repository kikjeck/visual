import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from celluloid import Camera
import streamlit.components.v1 as components


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
        ext = df[["Item", "Serving Size", 'Calories', 'Total Fat', 'Total Fat (% Daily Value)', 'Carbohydrates',
                  'Carbohydrates (% Daily Value)', "Protein", "Category"]]

        return smry, ext

    # how many items have more than 200 calories
    smry, ext = get_data()

    st.write(smry.sample(frac=1))

    """"
    # First chart - bar chart
    """
    """
    ## quite simple to understand :)
    """

    item = st.selectbox("Item", smry["Item"])
    st.write(item)
    c = smry[smry.Item == item].index[0]
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize= (6, 4))
    plt.title(smry.Item[c] + " (" + str(smry.Calories[c]) + "calories" + " )")
    height = smry.iloc[c, [2, 4, 6]]
    plt.bar(x=smry.iloc[c, [2, 4, 6]].index, height=height)
    bottom, top = plt.ylim()
    plt.ylim((bottom, top+10))
    for index, value in enumerate(smry.iloc[c, [2, 4, 6]]):
        plt.text(index - 0.05, value + 0.5, str(value))
    st.pyplot(fig)
    """

    ## Second chart

    """

    sns.set_theme()
    sns.set_style("dark")
    plt.style.use("dark_background")

    cat = st.selectbox("Category", smry["Category"].unique())
    var = "Calories"
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

    """

    # The same char, but interactive

    """
    fig = go.Figure()
    fig = px.bar(smry.sort_values(var), x="Item", y=var, animation_frame="Category", height=600)
    fig.update_xaxes(showticklabels=False)
    fig.add_hline(y=2500//2, line_color="red", annotation_text=f"a half of standart {var.lower()} consumption")
    fig["layout"].pop("updatemenus")
    st.plotly_chart(fig)


    """
    ## Animation: how nutrution changes with increase of calories
    """
    fig = plt.figure()
    camera = Camera(fig)
    labels = ["Total Fat", "Carbohydrates", "Protein"]
    for cal in range(100, 1250, 25):
        plt.pie(smry[((cal - 100) <= smry.Calories) * (smry.Calories <= (cal + 100))].mean()[[1, 3, 5]],
                colors=['C0', 'C1', 'C2'])
        plt.text(-1, 1, f"Calories: {cal}")
        plt.legend(labels)
        camera.snap()
    animation = camera.animate()
    ### FROM: https://gist.github.com/ischurov/fb00906c5704ebdd56ff13d7e02583e4
    components.html(animation.to_jshtml(), height=1000)
    ### END FROM

    """
    
    ## This chart helps to understand patterns of proteins, fats, carbohydrates allocation
    
    """
    fig, ax = plt.subplots(2, 2, figsize=(14, 14))
    # fig.suptitle('1 row x 2 columns axes with no data')
    sns.set_theme(style="dark")
    sns.scatterplot(data=ext, x="Total Fat", y="Carbohydrates", hue="Category", ax=ax[0, 0], edgecolor="black").set(
        xlim=(-1, 80))
    sns.scatterplot(data=ext, x="Total Fat", y="Protein", hue="Category", ax=ax[1, 0], legend=False, edgecolor="black").set(xlim=(-1, 80))
    sns.scatterplot(data=ext, x="Protein", y="Carbohydrates", hue="Category", ax=ax[0, 1], legend=False, edgecolor="black").set(
        xlim=(-1, 80))
    st.pyplot(fig)