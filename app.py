import streamlit as st
import pandas as pd
import plotly.express as px
import os

from src.gemini_ai import ask_gemini
from src.db_connection import load_data_from_mysql
from src.forecasting import create_sales_forecast

# Page configuration
st.set_page_config(
    page_title="InsightAI Analytics",
    page_icon="📊",
    layout="wide"
)

# Load dataset from MySQL
df = load_data_from_mysql()

# Convert date
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Title
st.title("📊 InsightAI - Business Analytics Dashboard")
st.markdown("### AI-Powered Sales and Business Intelligence Platform")

st.sidebar.header("📁 Upload Sales Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    file_name = uploaded_file.name

    if file_name.endswith(".csv"):
        uploaded_df = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        uploaded_df = pd.read_excel(uploaded_file)

    st.success(
        f"Successfully uploaded: {file_name}"
    )

    st.write(
        "Uploaded Data Preview"
    )

    st.dataframe(
        uploaded_df.head(),
        width="stretch"
    )

    # Use uploaded data for dashboard analysis
    df = uploaded_df.copy()

    # Convert date column
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Sidebar filters
st.sidebar.header("🔍 Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category))
]

# KPI Calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
profit_margin = (total_profit / total_sales) * 100

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "🛒 Total Orders",
    total_orders
)

col4.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()

# Sales by Region
col1, col2 = st.columns(2)

with col1:

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region",
        text_auto=True
    )

    st.plotly_chart(
        fig_region,
        width="stretch"
    )

with col2:

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(
        fig_category,
        width="stretch"
    )

# Monthly Sales Trend
monthly_sales = (
    filtered_df
    .assign(
        Month=filtered_df["Order_Date"].dt.to_period("M").astype(str)
    )
    .groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    title="📅 Monthly Sales Trend",
    markers=True
)

st.plotly_chart(
    fig_monthly,
    width="stretch"
)

# Top Products
top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product",
    orientation="h",
    title="🏆 Top Products by Sales",
    text_auto=True
)

st.plotly_chart(
    fig_products,
    width="stretch"
)

# Raw Data
with st.expander("📄 View Raw Data"):

    st.dataframe(
        filtered_df,
        width="stretch"
    )

# ==============================
# 🤖 AI BUSINESS ANALYST
# ==============================

st.divider()

st.header("🤖 AI Business Analyst")

st.write(
    "Ask questions about your sales data and get AI-powered business insights."
)

user_question = st.text_input(
    "Ask a question about your business data:"
)

if st.button("🤖 Ask Gemini"):

    if user_question:

        # Create data summary
        data_summary = f"""
        Total Sales: ₹{filtered_df['Sales'].sum():,.2f}
        Total Profit: ₹{filtered_df['Profit'].sum():,.2f}
        Total Orders: {len(filtered_df)}

        Top Product:
        {filtered_df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5)}

        Sales by Region:
        {filtered_df.groupby('Region')['Sales'].sum()}

        Profit by Category:
        {filtered_df.groupby('Category')['Profit'].sum()}

        Top Customers:
        {filtered_df.groupby('Customer_Name')['Sales'].sum().sort_values(ascending=False).head(5)}
        """

        with st.spinner("Gemini is analyzing your business data..."):

            answer = ask_gemini(
                user_question,
                data_summary
            )

        st.subheader("💡 AI Business Insight")

        st.write(answer)

    else:

        st.warning("Please enter a question first.")

# ==============================
# 📋 AI-GENERATED BUSINESS SUMMARY
# ==============================

st.divider()

st.header("📋 AI-Generated Business Summary")

st.write(
    "Generate an automatic summary of your current business performance using Gemini AI."
)

if st.button("✨ Generate Business Summary"):

    # Calculate important business metrics
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = len(filtered_df)

    top_product = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .idxmax()
    )

    top_region = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    top_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .idxmax()
    )

    # Create summary for Gemini
    business_summary = f"""
    Total Sales: ₹{total_sales:,.2f}
    Total Profit: ₹{total_profit:,.2f}
    Total Orders: {total_orders}

    Top-Selling Product: {top_product}
    Best-Performing Region: {top_region}
    Most Profitable Category: {top_category}

    Sales by Region:
    {filtered_df.groupby("Region")["Sales"].sum()}

    Sales by Product:
    {filtered_df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(5)}

    Profit by Category:
    {filtered_df.groupby("Category")["Profit"].sum()}
    """

    summary_prompt = f"""
    You are a professional Business Intelligence Analyst.

    Analyze the following business performance data:

    {business_summary}

    Generate a professional business summary with these sections:

    1. Executive Summary
    2. Sales Performance
    3. Profitability Analysis
    4. Top Performing Areas
    5. Business Recommendations

    Use clear and professional language.
    Mention important numbers from the data.
    Provide practical recommendations.
    """

    with st.spinner("🤖 Gemini is generating your business summary..."):

        ai_summary = ask_gemini(
            "Generate a professional business summary.",
            summary_prompt
        )

    st.subheader("📊 AI Business Report")

    st.markdown(ai_summary)

# ==============================
# 📈 SALES FORECASTING
# ==============================

st.divider()

st.header("📈 Sales Forecasting")

st.write(
    "Predict future sales using Machine Learning."
)

forecast_months = st.slider(
    "Select forecast period (months)",
    min_value=3,
    max_value=12,
    value=6
)

# Create forecast
forecast_df = create_sales_forecast(
    filtered_df,
    months_to_predict=forecast_months
)

if st.button("🔮 Generate Sales Forecast"):

    st.subheader("📊 Sales Forecast")

    fig_forecast = px.line(
        forecast_df,
        x="Order_Date",
        y="Sales",
        color="Type",
        markers=True,
        title="Actual vs Forecasted Sales"
    )

    fig_forecast.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales (₹)"
    )

    st.plotly_chart(
        fig_forecast,
        width="stretch"
    )

    st.subheader("🔮 Forecasted Sales")

    st.dataframe(
        forecast_df.tail(forecast_months),
        width="stretch"
    )


# ==============================
# 📊 FORECAST KPI CARDS
# ==============================

future_forecast = forecast_df[
    forecast_df["Type"] == "Forecast"
]

first_forecast = future_forecast["Sales"].iloc[0]
last_forecast = future_forecast["Sales"].iloc[-1]

growth_percentage = (
    (last_forecast - first_forecast)
    / first_forecast
) * 100

highest_sales = future_forecast["Sales"].max()

highest_month = future_forecast.loc[
    future_forecast["Sales"].idxmax(),
    "Order_Date"
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📈 Forecast Growth",
        f"{growth_percentage:.2f}%"
    )

with col2:
    st.metric(
        "🏆 Best Forecast Month",
        highest_month.strftime("%B %Y")
    )

with col3:
    st.metric(
        "💰 Highest Forecast Sales",
        f"₹{highest_sales:,.0f}"
    )

# ==============================
# 🤖 AI FORECAST ANALYSIS
# ==============================

st.subheader("🤖 AI Forecast Analysis")

if st.button("✨ Explain Forecast with Gemini"):

    future_forecast = forecast_df[
        forecast_df["Type"] == "Forecast"
    ]

    forecast_summary = future_forecast[
        ["Order_Date", "Sales"]
    ].to_string(index=False)

    forecast_prompt = f"""
    You are a professional Business Intelligence Analyst.

    Analyze this Machine Learning sales forecast:

    {forecast_summary}

    Provide a professional business analysis including:

    1. Overall sales trend
    2. Expected sales growth or decline
    3. Highest predicted sales month
    4. Business recommendations

    Mention important sales values in Indian Rupees.
    Use clear and professional language.
    """

    with st.spinner(
        "🤖 Gemini is analyzing the forecast..."
    ):

        forecast_analysis = ask_gemini(
            "Explain this sales forecast.",
            forecast_prompt
        )

    st.markdown(forecast_analysis)