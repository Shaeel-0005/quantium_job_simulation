import pandas as pd
import glob
import os

# Make sure we're pointing to correct folder
data_path = "data/daily_sales_data_*.csv"
files = glob.glob(data_path)

print("Files found:", files)

all_data = []

for file in files:
    df = pd.read_csv(file)

    # Normalize column names (just in case)
    df.columns = df.columns.str.lower()

    # Filter Pink Morsels (case-safe)
    df = df[df["product"].str.strip().str.lower() == "pink morsel"]

    if df.empty:
        print(f"No Pink Morsels in {file}")
        continue

    # Clean price
    df["price"] = df["price"].astype(str).str.replace("$", "", regex=False).astype(float)

    # Quantity numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Sales calculation
    df["sales"] = df["quantity"] * df["price"]

    # Keep required columns
    df = df[["sales", "date", "region"]]

    # Standardize names
    df.columns = ["Sales", "Date", "Region"]

    all_data.append(df)

# Combine safely
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("formatted_sales_output.csv", index=False)
    print("Done! File created.")
else:
    print("No data found after filtering.")