import pandas as pd

# Load dataset
df = pd.read_csv("data/sales_data.csv")

# Convert date column
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

print("\n========== DATASET OVERVIEW ==========")

print(f"Total Orders: {len(df)}")
print(f"Total Sales: ₹{df['Sales'].sum():,.2f}")
print(f"Total Cost: ₹{df['Cost'].sum():,.2f}")
print(f"Total Profit: ₹{df['Profit'].sum():,.2f}")

print("\n========== TOP PRODUCTS ==========")

top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(top_products)

print("\n========== SALES BY REGION ==========")

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(region_sales)

print("\n========== PROFIT BY CATEGORY ==========")

category_profit = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(category_profit)

print("\n========== TOP CUSTOMERS ==========")

top_customers = (
    df.groupby("Customer_Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(top_customers)

print("\n========== MONTHLY SALES ==========")

df["Month"] = df["Order_Date"].dt.to_period("M")

monthly_sales = (
    df.groupby("Month")["Sales"]
    .sum()
)

print(monthly_sales)