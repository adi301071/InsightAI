import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Number of records
NUM_RECORDS = 1000

# Sample data
products = {
    "Laptop": ("Electronics", 60000),
    "Smartphone": ("Electronics", 25000),
    "Headphones": ("Electronics", 3000),
    "Office Chair": ("Furniture", 12000),
    "Desk": ("Furniture", 18000),
    "Notebook": ("Stationery", 150),
    "Pen Set": ("Stationery", 250),
    "Backpack": ("Accessories", 1800),
    "Mouse": ("Accessories", 1200),
    "Keyboard": ("Accessories", 2500)
}

customers = [
    "Rahul Sharma",
    "Amit Verma",
    "Priya Singh",
    "Neha Gupta",
    "Rohit Tiwari",
    "Anjali Patel",
    "Vikas Kumar",
    "Sneha Joshi",
    "Karan Mehta",
    "Pooja Yadav"
]

regions = {
    "North": ["Delhi", "Chandigarh", "Jaipur"],
    "South": ["Hyderabad", "Bangalore", "Chennai"],
    "East": ["Kolkata", "Bhubaneswar", "Patna"],
    "West": ["Mumbai", "Pune", "Ahmedabad"]
}

payment_methods = ["Credit Card", "Debit Card", "UPI", "Cash", "Net Banking"]

data = []

start_date = datetime(2024, 1, 1)

for i in range(1, NUM_RECORDS + 1):

    product = random.choice(list(products.keys()))
    category, unit_price = products[product]

    region = random.choice(list(regions.keys()))
    city = random.choice(regions[region])

    quantity = random.randint(1, 5)

    sales = quantity * unit_price

    cost = sales * random.uniform(0.55, 0.80)

    profit = sales - cost

    order_date = start_date + timedelta(
        days=random.randint(0, 730)
    )

    data.append({
        "Order_ID": f"ORD-{i:05d}",
        "Order_Date": order_date,
        "Customer_Name": random.choice(customers),
        "Region": region,
        "City": city,
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Sales": round(sales, 2),
        "Cost": round(cost, 2),
        "Profit": round(profit, 2),
        "Payment_Method": random.choice(payment_methods)
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save dataset
df.to_csv("data/sales_data.csv", index=False)

print("Sales dataset created successfully!")
print(f"Total records: {len(df)}")
print(df.head())