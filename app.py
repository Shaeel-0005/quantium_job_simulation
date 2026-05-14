import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_sales_output.csv")

# Ensure correct types
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date (important for line chart)
df = df.sort_values("Date")

# Aggregate sales by date
daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

# Create line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    template="plotly_white"
)

# Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods - Pink Morsel Sales Visualiser"),

    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

if __name__ == "__main__":
    app.run(debug=False)