import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# -----------------------------
# Load and prepare data
# -----------------------------
df = pd.read_csv("formatted_sales_output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Region"] = df["Region"].str.lower()

# -----------------------------
# App setup
# -----------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Pink Morsels Analytics"

# -----------------------------
# Custom CSS - Injected via index_string (100% reliable)
# -----------------------------
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            * { margin: 0; padding: 0; box-sizing: border-box; }

            body {
                background: #05050a;
                color: #ffffff;
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                overflow-x: hidden;
            }

            .dashboard-wrapper {
                background: radial-gradient(1200px 600px at 20% 10%, #1a1025 0%, transparent 50%),
                            radial-gradient(800px 500px at 80% 80%, #100a1a 0%, transparent 50%),
                            #05050a;
                min-height: 100vh;
                padding: 2rem;
                max-width: 1400px;
                margin: 0 auto;
            }

            .header { text-align: center; margin-bottom: 2.5rem; animation: fadeUp 0.8s ease-out; }
            .title {
                font-size: 3.5rem; font-weight: 800; margin: 0;
                background: linear-gradient(135deg, #ff2a7c, #7928ca);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                letter-spacing: -1px;
            }
            .subtitle { color: #8a8a9a; font-size: 1.1rem; margin-top: 0.5rem; font-weight: 300; }

            .kpi-grid {
                display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.2rem; margin-bottom: 2rem;
            }
            .kpi-card {
                background: rgba(18, 18, 28, 0.65); 
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px; padding: 1.5rem; 
                backdrop-filter: blur(16px);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative; overflow: hidden;
            }
            .kpi-card::before {
                content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
                background: linear-gradient(90deg, #ff2a7c, #7928ca); opacity: 0.6;
            }
            .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 10px 40px rgba(255, 42, 124, 0.35); }
            .kpi-label { font-size: 0.85rem; color: #8a8a9a; text-transform: uppercase; letter-spacing: 1.5px; margin: 0; }
            .kpi-value { font-size: 2rem; font-weight: 700; margin: 0.4rem 0 0; color: #fff; }

            .main-layout {
                display: grid; grid-template-columns: 280px 1fr; gap: 1.5rem;
            }
            @media (max-width: 900px) { .main-layout { grid-template-columns: 1fr; } }

            .filter-panel {
                background: rgba(18, 18, 28, 0.65); 
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px; padding: 1.5rem; 
                backdrop-filter: blur(16px); height: fit-content;
            }
            .panel-title { font-size: 1.1rem; margin-bottom: 1.2rem; color: #8a8a9a; font-weight: 600; }

            .region-toggle { display: flex; flex-direction: column; gap: 0.6rem; }
            .region-option {
                background: rgba(255, 255, 255, 0.03); padding: 0.7rem 1rem; border-radius: 10px;
                cursor: pointer; transition: all 0.2s ease; border: 1px solid transparent; 
                font-weight: 500; color: #fff;
            }
            .region-option:hover { background: rgba(255, 255, 255, 0.06); }
            .region-option.active {
                background: #ff2a7c; border-color: #ff2a7c;
                box-shadow: 0 0 20px rgba(255, 42, 124, 0.35);
            }

            .chart-container {
                background: rgba(18, 18, 28, 0.65); 
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px; padding: 1.5rem; 
                backdrop-filter: blur(16px);
            }

            @keyframes fadeUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div([
    html.Div(className="dashboard-wrapper", children=[
        # Header
        html.Div(className="header", children=[
            html.H1(className="title", children="PINK MORSELS"),
            html.P(className="subtitle", children="Real-time Sales Analytics Dashboard")
        ]),

        # KPI Strip
        html.Div(className="kpi-grid", children=[
            html.Div(id="kpi-total", className="kpi-card"),
            html.Div(id="kpi-avg", className="kpi-card"),
            html.Div(id="kpi-range", className="kpi-card"),
            html.Div(id="kpi-region", className="kpi-card")
        ]),

        # Main Grid
        html.Div(className="main-layout", children=[
            # Filter Panel
            html.Div(className="filter-panel", children=[
                html.H4(className="panel-title", children="🌍 REGION FILTER"),
                html.Div(id="region-options", className="region-toggle")
            ]),

            # Chart Panel
            html.Div(className="chart-container", children=[
                dcc.Loading(
                    id="loading-chart",
                    type="circle",
                    color="#ff2a7c",
                    children=[
                        dcc.Graph(
                            id="sales-chart",
                            config={"displayModeBar": False},
                            style={"height": "450px"}
                        )
                    ]
                )
            ])
        ])
    ]),
    dcc.Store(id="selected-region", data="all")
])


# -----------------------------
# Callbacks
# -----------------------------
@callback(
    Output("region-options", "children"),
    Input("selected-region", "data")
)
def render_region_options(selected):
    regions = [
        ("all", "All Regions"),
        ("north", "North"),
        ("east", "East"),
        ("south", "South"),
        ("west", "West")
    ]

    options = []
    for value, label in regions:
        is_active = value == selected
        options.append(
            html.Div(
                label,
                className=f"region-option {'active' if is_active else ''}",
                n_clicks=0,
                id={'type': 'region-btn', 'index': value},
                style={'cursor': 'pointer'}
            )
        )
    return options


@callback(
    Output("selected-region", "data"),
    Input({'type': 'region-btn', 'index': dash.ALL}, "n_clicks"),
    prevent_initial_call=False
)
def update_selected_region(n_clicks):
    if not any(n_clicks):
        return "all"

    ctx = dash.callback_context
    if not ctx.triggered:
        return "all"

    triggered_id = ctx.triggered[0]['prop_id']
    import json
    btn_id = json.loads(triggered_id.split('.')[0])
    return btn_id['index']


@callback(
    [Output("kpi-total", "children"), Output("kpi-avg", "children"),
     Output("kpi-range", "children"), Output("kpi-region", "children")],
    Input("selected-region", "data")
)
def update_kpis(region):
    filt = df if region == "all" else df[df["Region"] == region]
    total = filt["Sales"].sum()
    avg = filt["Sales"].mean()
    d_min = filt["Date"].min().strftime("%b %Y")
    d_max = filt["Date"].max().strftime("%b %Y")
    reg_name = "All Regions" if region == "all" else region.title()

    kpi = lambda val, lbl: html.Div([
        html.P(lbl, className="kpi-label"),
        html.H3(val, className="kpi-value")
    ])
    return (
        kpi(f"${total:,.0f}", "Total Sales"),
        kpi(f"${avg:,.0f}", "Avg Daily"),
        kpi(f"{d_min} – {d_max}", "Period"),
        kpi(reg_name, "Active Filter")
    )


def create_chart(dataframe, region):
    grouped = dataframe.groupby("Date", as_index=False)["Sales"].sum()
    fig = px.line(grouped, x="Date", y="Sales", markers=True)

    fig.update_traces(
        line=dict(color="#ff2a7c", width=4),
        marker=dict(size=8, line=dict(width=2, color="#fff")),
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#a0a0b0"),
        margin=dict(l=40, r=20, t=10, b=40),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False, title="Sales Volume"),
        hoverlabel=dict(bgcolor="rgba(15,15,25,0.95)", bordercolor="#ff2a7c", font=dict(color="#fff"))
    )
    return fig


@callback(
    Output("sales-chart", "figure"),
    Input("selected-region", "data")
)
def update_chart(region):
    filt = df if region == "all" else df[df["Region"] == region]
    return create_chart(filt, region)


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)