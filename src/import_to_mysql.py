import pandas as pd
import mysql.connector

# Load CSV data
df = pd.read_csv("data/sales_data.csv")

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tiwari",
    database="insightai_db"
)

cursor = connection.cursor()

# Create sales table
create_table_query = """
CREATE TABLE IF NOT EXISTS sales (
    Order_ID VARCHAR(20) PRIMARY KEY,
    Order_Date DATE,
    Customer_Name VARCHAR(100),
    Region VARCHAR(50),
    City VARCHAR(100),
    Product VARCHAR(100),
    Category VARCHAR(100),
    Quantity INT,
    Unit_Price DECIMAL(12,2),
    Sales DECIMAL(12,2),
    Cost DECIMAL(12,2),
    Profit DECIMAL(12,2),
    Payment_Method VARCHAR(50)
)
"""

cursor.execute(create_table_query)

# Insert data
insert_query = """
INSERT INTO sales (
    Order_ID,
    Order_Date,
    Customer_Name,
    Region,
    City,
    Product,
    Category,
    Quantity,
    Unit_Price,
    Sales,
    Cost,
    Profit,
    Payment_Method
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():

    values = (
        row["Order_ID"],
        row["Order_Date"],
        row["Customer_Name"],
        row["Region"],
        row["City"],
        row["Product"],
        row["Category"],
        row["Quantity"],
        row["Unit_Price"],
        row["Sales"],
        row["Cost"],
        row["Profit"],
        row["Payment_Method"]
    )

    cursor.execute(insert_query, values)

# Save changes
connection.commit()

print("Data imported successfully!")
print(f"Total records imported: {len(df)}")

cursor.close()
connection.close()