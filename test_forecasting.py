from src.db_connection import load_data_from_mysql
from src.forecasting import create_sales_forecast

# Load data from MySQL
df = load_data_from_mysql()

# Create forecast
forecast_df = create_sales_forecast(
    df,
    months_to_predict=6
)

print("========== SALES FORECAST ==========")
print(forecast_df.tail(6))