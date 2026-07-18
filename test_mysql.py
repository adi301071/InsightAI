from src.db_connection import load_data_from_mysql

df = load_data_from_mysql()

print("Data loaded successfully from MySQL!")
print("Total records:", len(df))
print(df.head())