import pandas as pd
import plotly.express as px
import streamlit as st

# pip install plotly
# pip install streamlit

st.set_page_config(layout = "wide")  

st.title("📊 Sales Dashboard")

@st.cache_data
def load_data():
    df = pd.read_excel("Sales_Data_Large_2.xlsx")
    
    return df

df = load_data()

st.dataframe(
    df.head(100),
    use_container_width = True
)

years = sorted(df["Year"].unique())

selected_years = st.multiselect(
    "Select Years",
    options = years,
    default = years
)

filtered_df = df[ df["Year"].isin(selected_years) ]

countries = sorted(df["Country"].unique())

selected_countries = st.multiselect(
    "Select Countries",
    options = countries,
    default = countries
)

filtered_df = filtered_df[ filtered_df["Country"].isin(selected_countries) ]

st.markdown("### 📌 KPI")

total_sales = filtered_df["TotalSales"].sum()
units_sold = filtered_df["Quantity"].sum()
order_count = filtered_df["OrderID"].nunique()
average_order_value = total_sales / order_count

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("💰 Total Sales",  f"{total_sales:,.0f}")

with kpi2:
    st.metric("Units Sold", f"{units_sold:,.0f}")

with kpi3:
    st.metric("Average Order Value", f"{average_order_value:,.0f}")
    
st.markdown("### 📈 Charts")

sales_by_city = (
    filtered_df.groupby("City")["TotalSales"].sum()
    .reset_index()
    .sort_values(by="TotalSales", ascending=False)
)

sales_by_country =  (
    filtered_df.groupby("Country")["TotalSales"].sum()
    .reset_index()
    .sort_values(by="TotalSales", ascending=False)
)

top_products = (
    filtered_df.groupby("ProductName")["TotalSales"].sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

monthly_sales = (
    filtered_df.groupby(["Year", "Month"])["TotalSales"].sum()
    .reset_index()    
)

sales_by_payment =( 
    filtered_df.groupby("PaymentMethod")["TotalSales"].sum()
    .reset_index()
)

col1,col2 = st.columns(2)


with col1:
    fig1=px.bar(
        sales_by_city,
        x="TotalSales",
        y="City",
        orientation= "h",
        title="Sales by City",
        text_auto= '.2s'

    )

    fig1.update_traces( textfont_color = "white", textposition = "outside")
    st.plotly_chart(fig1, use_container_width=True)


with col2:
    fig2=px.bar(
        sales_by_country,
        x="Country",
        y="TotalSales",
        orientation= "h",
        title="Sales by Country",
        text_auto= '.2s'

    )

    fig2.update_traces( textfont_color = "white", textposition = "outside")
    st.plotly_chart(fig2, use_container_width=True)


col3,col4 = st.columns(2)


with col3:
    fig3 = px.bar(
        top_products,
        x="ProductName",
        y="TotalSales",
        title="Top 5 Products",
        text_auto= '.2s'

    )

    fig3.update_traces( textfont_color = "white", textposition = "outside")
    st.plotly_chart(fig3, use_container_width=True)


with col4:
    fig4 = px.line(
        monthly_sales,
        x = "Month",
        y = "TotalSales",
        color = "Year",
        markers = True,
        title = "Monthly Sales Trend",
        text = "TotalSales"
    )
    
    fig4.update_traces(textposition = "top center", texttemplate = '%{text:.2s}')
    st.plotly_chart(fig4, use_container_width = True)

col5, col6 =st.columns(2)

with col5:
    fig5=px.pie(
        sales_by_payment,
        names = "PaymentMethod",
        values = "TotalSales",
        title = "Total Sales by Payment Method",
        hole = 0,
        color_discrete_sequence= px.colors.sequential.Blues
    )

    fig5.update_traces(textinfo = "percent")
    st.plotly_chart(fig5, use_container_width= True)

    
with col6:
    fig6=px.pie(
        sales_by_payment,
        names = "PaymentMethod",
        values = "TotalSales",
        title = "Total Sales by Payment Method",
        hole = 0.6,
        color_discrete_sequence= px.colors.sequential.Greens
    )

    fig6.update_traces(textinfo = "percent")
    st.plotly_chart(fig6, use_container_width= True)