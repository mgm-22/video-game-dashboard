# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:54:36 2026

@author: Grace
"""
# ----------------------------------------------------------
# VIDEO GAME MARKET INTELLIGENCE DASHBOARD
# MBAN626 Dashboard Project
# ----------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------

st.set_page_config(
    page_title="Video Game Market Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------
# PROFESSIONAL GAMING DASHBOARD STYLE
# ----------------------------------------------------------

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Russo+One&family=Orbitron:wght@500;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">

<style>

/* 1. REMOVE WHITE SPACE & DEFAULT HEADER */
/* Hide header but keep sidebar toggle button */
header {
    background: transparent !important;
}

/* Style the sidebar toggle icon */
button[kind="header"] {
    color: #8f96a3 !important;
}

button[kind="header"]:hover {
    color: white !important;
}

/* 2. THE RGB NEON GRADIENT STRIP (Pink, Cyan, Orange) */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 8px;
    background: linear-gradient(90deg, #f44786, #61d5f3, #ffcb85, #f44786);
    background-size: 300% 300%;
    animation: neonFlow 8s ease infinite;
    z-index: 9999;
    box-shadow: 0 0 15px rgba(244, 71, 134, 0.4);
}

@keyframes neonFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* GLOBAL STYLES */
.stApp {
    background: #141416 !important; 
    color: white;
    font-family: 'Inter', sans-serif;
}

/* GLASSMORPHISM SIDEBAR */
/* Base sidebar container */
section[data-testid="stSidebar"] {
    background: transparent !important;
    border: none !important;
}

/* Floating glass sidebar */
section[data-testid="stSidebar"] > div:first-child {
    background: rgba(18,18,22,0.88);
    backdrop-filter: blur(18px);
    border-radius: 28px;
    padding: 22px 18px;

    border: 1px solid rgba(255,255,255,0.06);

    box-shadow:
        0 0 18px rgba(244,71,134,0.15),
        0 0 28px rgba(97,213,243,0.08),
        inset 0 0 30px rgba(0,0,0,0.45);
}

/* Proper spacing between sidebar widgets */
section[data-testid="stSidebar"] .stTextInput,
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider {
    margin-bottom: 18px;
}

section[data-testid="stSidebar"] svg {
    color: #8f96a3 !important;
    fill: #8f96a3 !important;
    stroke: #8f96a3 !important;

    filter: none !important;
    text-shadow: none !important;
}

/* Hover effect (clean white highlight) */
section[data-testid="stSidebar"] svg:hover {
    color: white !important;
    fill: white !important;
    stroke: white !important;
}

/* Remove neon effects from sidebar only */
section[data-testid="stSidebar"] * {
    text-shadow: none !important;
}
    
    
/* Search + Dropdown inputs */

.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background: #1b1b20 !important;
    border-radius: 12px !important;
    border: 1px solid #2a2a33 !important;
    color: white !important;
}

/* Input focus glow */

.stTextInput input:focus,
.stSelectbox div[data-baseweb="select"]:focus-within {
    border: 1px solid #f44786 !important;
    box-shadow: 0 0 10px rgba(244,71,134,0.4);
}

/* PINK NEON SLIDER */
div[data-testid="stSlider"] div[role="slider"] {
    background: #f44786 !important;
    border: none !important;
    box-shadow: 0 0 12px #f44786;
}

div[data-baseweb="slider"] > div:first-child > div {
    background: linear-gradient(90deg,#f44786,#ffacdd) !important;
    height:4px !important;
}

/* HERO SECTION */
.hero-container {
    background: linear-gradient(135deg, #232326 0%, #141416 100%);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid #2a2a2e;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 4px;
    background: #f44786;
    box-shadow: 0 0 20px #f44786;
}

.chart-container, .kpi-card {
    background: #1c1c1f !important;
    border-radius: 16px !important;
    border: 1px solid rgba(244,71,134,0.3) !important;
    padding: 20px 24px !important;
    transition: all 0.35s ease;
    margin-bottom: 20px;

    /* Soft RGB glow */
    box-shadow:
        0 0 10px rgba(244,71,134,0.15),
        0 0 15px rgba(97,213,243,0.1),
        0 0 20px rgba(255,203,133,0.08);
}

.chart-container:hover, .kpi-card:hover {
    transform: translateY(-5px);
    border-color: transparent;
    box-shadow: 0 0 25px rgba(244,71,134,0.5),
                0 0 35px rgba(97,213,243,0.4),
                0 0 45px rgba(255,203,133,0.3);
}

.chart-header {
    font-family: 'Orbitron', sans-serif;
    color: #61d5f3;
    font-size: 16px;
    letter-spacing: 1px;
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: 1px solid #2a2a33;
}

/* RGB Neon Gradient Title */
.neon-title {
    font-family: 'Russo One', sans-serif;
    font-size: 100px;
    letter-spacing: 1px;
    margin: 0;
    font-weight: 600;

    background: linear-gradient(
        90deg,
        #f44786 0%,
        #b07cc6 25%,
        #61d5f3 50%,
        #ffcb85 75%,
        #f44786 100%
    );

    background-size: 400% 100%;
    animation: neonFlow 10s linear infinite;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 6px rgba(244,71,134,0.35),
        0 0 12px rgba(97,213,243,0.25);
}

/* TYPOGRAPHY */
.sub-title {
    font-family: 'Orbitron', sans-serif;
    color: #61d5f3;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 15px;
}
.kpi-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 26px;
    color: #ffc5d9;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #888891;
    padding: 30px 0;
    font-size: 13px;
    border-top: 1px solid #2a2a33;
    margin-top: 50px;
}

</style>


<style>

/* LEADERBOARD TABLE CUSTOMS */
.leaderboard-card {
    background: #111119;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2a2a33;
}

.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    color: white;
}

.leaderboard-table th {
    text-align: left;
    padding: 12px;
    color: #ffcb85;
    border-bottom: 2px solid #2a2a33;
}

.leaderboard-table td {
    padding: 12px;
    border-bottom: 1px solid #1f1f2b;
}

.platform-badge {
    background: #f44786;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("vgsales.csv")

    df = df.drop(columns=["Rank"])

    df = df.dropna(subset=["Year"])

    df["Year"] = df["Year"].astype(int)

    return df


df = load_data()

# ----------------------------------------------------------
# CONTROL FLOW FUNCTION
# ----------------------------------------------------------

def classify_sales(global_sales):

    if global_sales >= 20:
        return "Blockbuster"

    elif global_sales >= 10:
        return "Very Popular"

    elif global_sales >= 5:
        return "Popular"

    else:
        return "Standard"


df["Sales_Category"] = df["Global_Sales"].apply(classify_sales)

# ----------------------------------------------------------
# CUSTOM FUNCTIONS
# ----------------------------------------------------------

def top_selling_games(data, n=10):

    return data.sort_values(
        "Global_Sales",
        ascending=False
    ).head(n)


def regional_sales(data):

    regions = {
        "North America": data["NA_Sales"].sum(),
        "Europe": data["EU_Sales"].sum(),
        "Japan": data["JP_Sales"].sum(),
        "Other": data["Other_Sales"].sum()
    }

    return pd.DataFrame(
        list(regions.items()),
        columns=["Region","Sales"]
    )

# ----------------------------------------------------------
# CLASS IMPLEMENTATION
# ----------------------------------------------------------

class VideoGameAnalyzer:

    def __init__(self, dataframe):
        self.df = dataframe

    def total_games(self):
        return len(self.df)

    def total_sales(self):
        return self.df["Global_Sales"].sum()

    def avg_sales(self):
        return self.df["Global_Sales"].mean()

    def best_genre(self):
        return self.df.groupby("Genre")["Global_Sales"].sum().idxmax()

    def top_platform(self):
        return self.df.groupby("Platform")["Global_Sales"].sum().idxmax()


analyzer = VideoGameAnalyzer(df)

# ----------------------------------------------------------
# SIDEBAR FILTERS & SEARCH
# ----------------------------------------------------------

st.sidebar.markdown("""
<div style="
font-family: 'Orbitron';
font-size:18px;
color:#61d5f3;
letter-spacing:1px;
margin-bottom:10px;">
NAVIGATION & FILTERS
</div>
""", unsafe_allow_html=True)

# ADDED SEARCH BAR
search_query = st.sidebar.text_input("SEARCH GAME TITLES", placeholder="e.g. Animal Crossing")

genre_filter = st.sidebar.selectbox("SELECT GENRE", ["All"] + sorted(df["Genre"].unique()))
platform_filter = st.sidebar.selectbox("SELECT PLATFORM", ["All"] + sorted(df["Platform"].unique()))
year_range = st.sidebar.slider("YEAR RANGE", int(df["Year"].min()), int(df["Year"].max()), (2000, 2020))

filtered_df = df.copy()

# Apply Filters
if search_query:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search_query, case=False, na=False)]
if genre_filter != "All":
    filtered_df = filtered_df[filtered_df["Genre"] == genre_filter]
if platform_filter != "All":
    filtered_df = filtered_df[filtered_df["Platform"] == platform_filter]
filtered_df = filtered_df[(filtered_df["Year"] >= year_range[0]) & (filtered_df["Year"] <= year_range[1])]


# ----------------------------------------------------------
# KPI values based on filtered data
# ----------------------------------------------------------

total_games = len(filtered_df)
total_sales = filtered_df["Global_Sales"].sum()
avg_sales = filtered_df["Global_Sales"].mean() if not filtered_df.empty else 0
best_genre = filtered_df.groupby("Genre")["Global_Sales"].sum().idxmax() if not filtered_df.empty else "N/A"


# ----------------------------------------------------------
# HERO HEADER
# ----------------------------------------------------------


col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<h1 class="neon-title">MARKET OVERVIEW</h1>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-top: 15px; display: flex; align-items: center; gap: 15px;">
        <div style="background: #f44786; height: 20px; width: 4px; border-radius: 2px;"></div>
        <span style="color: #61d5f3; font-family: 'Orbitron'; font-size: 14px;">DOMINANT STRATEGY:</span>
        <span style="color: white; font-weight: 500;">{best_genre.upper()}</span>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
    <div style="text-align: right;">
        <p style="color: #888891; font-size: 12px; margin: 0;">MBAN626 DASHBOARD PROJECT</p>
        <h2 style="color: white; font-size: 36px; margin: 5px 0; font-family: Orbitron;">{total_games:,}</h2>
        <p style="color: #61d5f3; font-size: 12px; margin: 0;">● NUMBER OF GAMES</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------
# KPI METRICS & API
# ----------------------------------------------------------

try:
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    php_rate = response.json()["rates"]["PHP"]
except:
    php_rate = 56.0

sales_php = total_sales * php_rate

col1, col2, col3 = st.columns(3)

metrics = [
    ("Global Sales (USD)", f"${total_sales:,.1f}M"),
    ("Global Sales (PHP)", f"₱{sales_php:,.1f}M"),
    ("Avg. Game Sales", f"{avg_sales:.2f}M")
]

for col, (label, value) in zip([col1, col2, col3], metrics):
    with col:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True
        )


# ----------------------------------------------------------
# FUNCTION: TOP SELLING GAMES
# ----------------------------------------------------------

def top_games(data, n=10):

    return data.sort_values(
        by="Global_Sales",
        ascending=False
    ).head(n)

top_games_chart = top_games(filtered_df)

def get_map_data(df):
    # Summing up sales by region
    regional_totals = {
        "North America": df["NA_Sales"].sum(),
        "Europe": df["EU_Sales"].sum(),
        "Japan": df["JP_Sales"].sum(),
        "Rest of World": df["Other_Sales"].sum()
    }
    
    # Mapping specific ISO codes to the regions in your CSV
    mapping = [
        {"Country": "USA", "ISO": "USA", "Region": "North America", "Sales": regional_totals["North America"]},
        {"Country": "Canada", "ISO": "CAN", "Region": "North America", "Sales": regional_totals["North America"]},
        {"Country": "Japan", "ISO": "JPN", "Region": "Japan", "Sales": regional_totals["Japan"]},
        {"Country": "United Kingdom", "ISO": "GBR", "Region": "Europe", "Sales": regional_totals["Europe"]},
        {"Country": "Germany", "ISO": "DEU", "Region": "Europe", "Sales": regional_totals["Europe"]},
        {"Country": "France", "ISO": "FRA", "Region": "Europe", "Sales": regional_totals["Europe"]},
        {"Country": "Australia", "ISO": "AUS", "Region": "Rest of World", "Sales": regional_totals["Rest of World"]},
        {"Country": "Brazil", "ISO": "BRA", "Region": "Rest of World", "Sales": regional_totals["Rest of World"]}
    ]
    return pd.DataFrame(mapping)

# ----------------------------------------------------------
# CHART SETTINGS & THEME
# ----------------------------------------------------------

# Custom palette for visual appeal
palette = ["#ffc5d9", "#c2f2d0", "#fdf5c9", "#249f9c", "#ffcb85", "#f44786"]

# Unified layout to ensure consistent fonts and colors across all charts
chart_layout = dict(
    font=dict(family="Inter", color="white", size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        gridcolor="#2a2a33", 
        title_font=dict(family="Orbitron", color="#61d5f3")
    ),
    yaxis=dict(
        gridcolor="#2a2a33", 
        title_font=dict(family="Orbitron", color="#61d5f3")
    ),
    # Add this block to fix the legend font color
    legend=dict(
        font=dict(color="white")
    )
)

# ----------------------------------------------------------
# ROW 1: GLOBAL SALES TREND WITH KPI BOX
# ----------------------------------------------------------

# Create two columns: 4/5 for the chart, 1/5 for the KPI box
col_chart, col_kpi = st.columns([4, 1])

with col_chart:
    
    st.markdown('<p class="sub-title">Global Sales Trend by Top 10 Publishers</p>', unsafe_allow_html=True)

    if not filtered_df.empty:
        trend_data = filtered_df.groupby(['Year', 'Publisher'])['Global_Sales'].sum().reset_index()
        top_pubs = filtered_df.groupby('Publisher')['Global_Sales'].sum().nlargest(10).index
        trend_data = trend_data[trend_data['Publisher'].isin(top_pubs)]

        fig_line = px.line(
            trend_data, 
            x="Year", 
            y="Global_Sales", 
            color="Publisher",
            markers=True,
            color_discrete_sequence=["#f44786", "#61d5f3", "#ffcb85", "#c2f2d0", "#ffc5d9"]
        )
        
        fig_line.update_layout(**chart_layout)
        fig_line.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=430,
            showlegend=True,
            legend=dict(font=dict(size=9), orientation="h", y=-0.3, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No data available.")

with col_kpi:
    # Calculating a specific metric for the box (e.g., Year-over-Year change or Peak Sales)
    peak_sales = trend_data['Global_Sales'].max() if not filtered_df.empty else 0
    
    st.markdown(f"""
        <div class="chart-container" style="height:300px; display:flex; flex-direction:column; justify-content:center; align-items:center;">        <p style="color: #f44786; font-family: 'Orbitron'; font-size: 12px; letter-spacing: 1px; margin-bottom: 10px;">PEAK PERFORMANCE</p>
        <h2 style="color: white; font-family: 'Orbitron'; font-size: 32px; margin: 0;">${peak_sales:.1f}M</h2>
        <p style="color: #888891; font-size: 11px; margin-top: 10px;">HISTORIC ANNUAL HIGH</p>
        <div style="margin-top: 30px; width: 50px; height: 2px; background: #f44786; box-shadow: 0 0 10px #f44786;"></div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------
# ROW 2: STRATEGIC INSIGHTS (Charts 2 & 3)
# ----------------------------------------------------------

c1, c2 = st.columns(2)

with c1:
    # CHART 2: Genre vs Platform Heatmap (3-Color Tone Update)

    st.markdown('<p class="sub-title">Platform vs. Genre Opportunity Matrix</p>', unsafe_allow_html=True)
    
    if not filtered_df.empty:
        heatmap_data = filtered_df.pivot_table(index="Genre", columns="Platform", values="Global_Sales", aggfunc="sum").fillna(0)
        
        # 3-Tone Scale: Pink -> Cyan -> Orange (with a dark starting point)
        # Using codes: #f44786 (Pink), #61d5f3 (Cyan), #ffcb85 (Orange)
        three_tone_scale = [
            [0.0, "#141416"],   # Deep dark base
            [0.33, "#f44786"],  # Low Sales: Neon Pink
            [0.66, "#61d5f3"],  # Mid Sales: Cyan Blue
            [1.0, "#ffcb85"]    # High Sales: Soft Orange
        ]
        
        fig_heat = px.imshow(
            heatmap_data, 
            color_continuous_scale=three_tone_scale,
            aspect="auto"
        )
        
        fig_heat.update_layout(
            **chart_layout,
            coloraxis_colorbar=dict(
                title="Sales ($M)",
                thicknessmode="pixels", thickness=15,
                lenmode="fraction", len=0.8
            )
        )
        
        st.plotly_chart(fig_heat, use_container_width=True)



with c2:
    # CHART 3: Regional Comparison (Grouped Bar)

    st.markdown('<p class="sub-title">Regional Sales Performance by Genre</p>', unsafe_allow_html=True)
    reg_comp = filtered_df.groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales"]].sum().reset_index()
    reg_melt = reg_comp.melt(id_vars="Genre", var_name="Region", value_name="Sales")
    fig_reg_bar = px.bar(reg_melt, x="Genre", y="Sales", color="Region", barmode="group", 
                         color_discrete_map={"NA_Sales": "#f44786", "EU_Sales": "#61d5f3", "JP_Sales": "#ffcb85"})
    fig_reg_bar.update_layout(**chart_layout)
    st.plotly_chart(fig_reg_bar, use_container_width=True)



# ----------------------------------------------------------
# ROW 3: EFFICIENCY & MAP (Chart 4 & 5)
# ----------------------------------------------------------

c3, c4 = st.columns(2)

with c3:
    # CHART 4: Publisher Efficiency (Bubble Chart)
    
    st.markdown('<p class="sub-title">Publisher Efficiency: Volume vs. Average Sales</p>', unsafe_allow_html=True)
    pub_stats = filtered_df.groupby("Publisher").agg({"Global_Sales": ["sum", "mean", "count"]}).reset_index()
    pub_stats.columns = ["Publisher", "Total_Sales", "Avg_Sales", "Game_Count"]
    top_pubs = pub_stats.nlargest(20, "Total_Sales")
    fig_bubble = px.scatter(top_pubs, x="Game_Count", y="Avg_Sales", size="Total_Sales", color="Publisher",
                            hover_name="Publisher", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_bubble.update_layout(**chart_layout, showlegend=False)
    st.plotly_chart(fig_bubble, use_container_width=True)
    

with c4:
    # CHART 5: Regional Market Map

    st.markdown('<p class="sub-title">Global Market Distribution</p>', unsafe_allow_html=True)
    
    region_colors = {
        "North America": "#f44786",
        "Europe": "#61d5f3",
        "Japan": "#ffcb85",
        "Rest of World": "#c2f2d0"
    }

    map_data = pd.DataFrame([
        {"ISO": "USA", "Region": "North America", "Sales": filtered_df["NA_Sales"].sum()},
        {"ISO": "CAN", "Region": "North America", "Sales": filtered_df["NA_Sales"].sum()},
        {"ISO": "JPN", "Region": "Japan", "Sales": filtered_df["JP_Sales"].sum()},
        {"ISO": "GBR", "Region": "Europe", "Sales": filtered_df["EU_Sales"].sum()},
        {"ISO": "DEU", "Region": "Europe", "Sales": filtered_df["EU_Sales"].sum()},
        {"ISO": "FRA", "Region": "Europe", "Sales": filtered_df["EU_Sales"].sum()},
        {"ISO": "AUS", "Region": "Rest of World", "Sales": filtered_df["Other_Sales"].sum()},
        {"ISO": "BRA", "Region": "Rest of World", "Sales": filtered_df["Other_Sales"].sum()}
    ])
    
    fig_map = px.choropleth(
        map_data, 
        locations="ISO", 
        color="Region", 
        hover_data={"Sales": ":.2f", "ISO": False, "Region": False},
        color_discrete_map=region_colors
    )
    
    # FIX: Update layout by unpacking chart_layout first, 
    # then explicitly setting the specific legend position for the map.
    fig_map.update_layout(
        **chart_layout
    )
    
    # Overwrite the legend position separately to avoid the "multiple values" error
    fig_map.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            font=dict(size=10)
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    fig_map.update_geos(
        bgcolor="rgba(0,0,0,0)", 
        showcountries=True, 
        countrycolor="#2a2a2e", 
        showocean=True, 
        oceancolor="#0f0f18",
        projection_type="natural earth",
        showframe=False
    )
    
    st.plotly_chart(fig_map, use_container_width=True)



# ----------------------------------------------------------
# FINAL ROW: LEADERBOARD TABLE
# ----------------------------------------------------------

st.markdown('<p class="sub-title">Top Selling Video Games Leaderboard</p>', unsafe_allow_html=True)
table_html = """<div class="chart-container"><table class="leaderboard-table">
<thead><tr><th>#</th><th>Game</th><th>Platform</th><th>Genre</th><th>Publisher</th><th>Global Sales</th></tr></thead><tbody>"""

for idx, row in top_games_chart.iterrows():
    table_html += f"""<tr><td>{idx+1}</td><td>{row['Name']}</td><td><span class="platform-badge">{row['Platform']}</span></td>
    <td>{row['Genre']}</td><td>{row['Publisher']}</td><td style="color:#ffcb85; font-weight:bold;">${row['Global_Sales']:,.2f}M</td></tr>"""

table_html += "</tbody></table></div>"
st.markdown(table_html, unsafe_allow_html=True)

# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------

st.markdown("""
<div style="text-align: center; color: #888891; padding: 20px; font-size: 13px; border-top: 1px solid #2a2a33; margin-top: 50px;">
    MBAN626 • AI and Data Analytics Strategy • 2T 2025–2026 
    &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 
    Dataset: Video Game Sales • Source: Kaggle / VGChartz
</div>
""", unsafe_allow_html=True)
