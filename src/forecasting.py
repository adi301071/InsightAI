import pandas as pd
from sklearn.linear_model import LinearRegression


def create_sales_forecast(df, months_to_predict=6):

    # Convert Order_Date to datetime
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    # Create monthly sales
    monthly_sales = (
        df.groupby(
            df["Order_Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    # Convert period to timestamp
    monthly_sales["Order_Date"] = (
        monthly_sales["Order_Date"]
        .dt.to_timestamp()
    )

    # Create numerical time feature
    monthly_sales["Month_Number"] = range(
        len(monthly_sales)
    )

    # Features and target
    X = monthly_sales[["Month_Number"]]
    y = monthly_sales["Sales"]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Create future months
    last_month_number = monthly_sales["Month_Number"].max()

    future_month_numbers = range(
        last_month_number + 1,
        last_month_number + 1 + months_to_predict
    )

    # Predict future sales
    future_sales = model.predict(
        pd.DataFrame(
            future_month_numbers,
            columns=["Month_Number"]
        )
    )

    # Create future dates
    last_date = monthly_sales["Order_Date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=months_to_predict,
        freq="MS"
    )

    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        "Order_Date": future_dates,
        "Sales": future_sales,
        "Type": "Forecast"
    })

    # Add type to historical data
    monthly_sales["Type"] = "Actual"

    # Combine actual and forecast data
    result = pd.concat(
        [
            monthly_sales[
                ["Order_Date", "Sales", "Type"]
            ],
            forecast_df
        ],
        ignore_index=True
    )

    return result