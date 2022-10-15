"""Calculate the average cost of a gallon of diesel over the years.

First source: US Department of Agriculture
  - Description: https://agtransport.usda.gov/Fuel/Historical-Diesel-Fuel-Prices/u2kh-s8ke
  - Download: https://agtransport.usda.gov/api/views/x88w-atzp/rows.csv?accessType=DOWNLOAD
"""
from typing import TypedDict
import requests
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt

PRICE_DATA_FILE_PATH = "./downloads/usda-gas-prices.csv"
PRICE_DATA_DOWNLOAD_URL = (
    "https://agtransport.usda.gov/api/views/x88w-atzp/rows.csv?accessType=DOWNLOAD"
)

# Actually, this webpage has some good data already cooked up about the price of gasoline over time.
# https://www.usinflationcalculator.com/inflation/gasoline-inflation-in-the-united-states/
# They got it from the BLS. I wonder if the BLS also has diesel prices over time.
#
# See https://fred.stlouisfed.org/tags/series?t=bls%3Bdiesel
# See https://fred.stlouisfed.org/graph/?g=UR2p
# Download url: https://fred.stlouisfed.org/graph/fredgraph.csv?id=WPU057303
FRED_DATA_FILE_PATH = "./downloads/fred-deisel-index.csv"
FRED_DATA_DOWNLOAD_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=WPU057303"


def download_as_needed(url: str, path: str):
    if not os.path.exists(path):
        result = requests.get(url)
        result.raise_for_status()
        with open(path, "w") as f:
            f.write(result.text)


download_as_needed(FRED_DATA_DOWNLOAD_URL, FRED_DATA_FILE_PATH)
download_as_needed(PRICE_DATA_DOWNLOAD_URL, PRICE_DATA_FILE_PATH)

# Date,Week,Month,Year,Region,Diesel Price
raw_prices_df: pd.DataFrame = pd.read_csv(PRICE_DATA_FILE_PATH)

# Calculate the average price for each month.
class MonthPrice(TypedDict):
    price: float
    date: datetime.date


monthly_prices: list[MonthPrice] = []
for (year, month), rows in raw_prices_df.groupby(["Year", "Month"]):
    month_start = datetime.date(year=year, month=month, day=1)
    average_price = rows["Diesel Price"].mean()
    monthly_prices.append(MonthPrice(price=average_price, date=month_start))

monthly_prices_df = pd.DataFrame(data=monthly_prices)

# DATE,WPU057303
fred_index_df: pd.DataFrame = pd.read_csv(FRED_DATA_FILE_PATH).rename(
    {"DATE": "date", "WPU057303": "price_index"}, axis="columns"
)
fred_index_df["date"] = fred_index_df["date"].apply(datetime.date.fromisoformat)

joined = monthly_prices_df.set_index("date").join(
    fred_index_df.set_index("date"), how="inner"
)
print(joined.head())

ratio: pd.Series = joined["price"] / joined["price_index"]
print(ratio.describe())
plot = ratio.plot.line()
plt.title("Price / Index of Diesel")
plt.show()
