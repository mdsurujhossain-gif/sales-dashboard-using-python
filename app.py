
import pandas as pd 
import streamlit as st
import plotly.express as px



# stramlit dashboard

st.set_page_config(page_title="Sales Dashboard",page_icon=":bar_chart:",layout="wide")


@st.cache  # this line cache the data when reloadin from web.

def get_excel_data():

    df = pd.read_excel(
        io = 'supermarket_sales.xlsx',
        engine= 'openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,

    )

    # Adding hour column to dataframe
    df["Hour"] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    return df

df = get_excel_data()


# side bar

st.sidebar.header("Please filter here")
city = st.sidebar.multiselect(
    "select the city:",
    options=df["City"].unique(),
    default=df["City"].unique()

)

customer_type = st.sidebar.multiselect(
    "select customer type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()

)

gender = st.sidebar.multiselect(
    "select the gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()

)

#filter functinality

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

st.dataframe(df_selection)


# main page

st.title(":bar_chart:Sales Dashboard")
st.markdown("##")

#top kpi's

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sales_by_transaction = round(df_selection["Total"].mean(),2)

# adding the vaiable in three column in dashboard

left_column, middle_column,right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales}")

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average sales by transaction")
    st.subheader(f"US $ {average_sales_by_transaction}")

st.markdown("---")



# sales by product line barchart
sales_by_productline =  df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")

fig_product_sales = px.bar(
    sales_by_productline,
    x="Total",
    y= sales_by_productline.index,
    orientation="h",
    title="<b> Sales by product line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_productline),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor ="rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))

)

#st.plotly_chart(fig_product_sales)


# Sales by hour

sales_by_hour =  df_selection.groupby(by=["Hour"]).sum()[["Total"]].sort_values(by="Total")


fig_product_sales_by_hour = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y= "Total",
    title="<b> Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

fig_product_sales_by_hour.update_layout(
    xaxis = (dict(tickmode="linear")),
    plot_bgcolor ="rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False))

)

# adding two graph to two columns.

left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales,use_container_width = True)
right_column.plotly_chart(fig_product_sales_by_hour,use_container_width = True)

# hide streamlit style
hide_st_style = """
                <style>
                #Mainmenu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>

"""
st.markdown(hide_st_style,unsafe_allow_html=True)