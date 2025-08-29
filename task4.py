import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------
# Page Configuration
# --------------------
st.set_page_config(page_title="IPL Dashboard", layout="wide")

# --------------------
# Title
# --------------------
st.title("🏏 IPL Data Analysis Dashboard")

# --------------------
# Load Datasets
# --------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("C:\\Users\\supri\\Downloads\\matches.csv")
    deliveries = pd.read_csv("C:\\Users\\supri\\Downloads\\deliveriesextracted.csv\\deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# --------------------
# Sidebar Filters
# --------------------
st.sidebar.header("Filter Options")
season = st.sidebar.selectbox("Select Season", sorted(matches['Season'].unique()))

# Filter matches for the selected season
season_matches = matches[matches['Season'] == season]

# --------------------
# Top Run Scorers
# --------------------
top_scorers = (
    deliveries[deliveries['match_id'].isin(season_matches['id'])]
    .groupby("batsman")["batsman_runs"]
    .sum()
    .reset_index()
    .sort_values(by="batsman_runs", ascending=False)
    .head(10)
)

st.subheader(f"Top 10 Run Scorers - {season}")
st.plotly_chart(px.bar(
    top_scorers,
    x="batsman",
    y="batsman_runs",
    color="batsman_runs",
    color_continuous_scale="Blues",
    title=f"Top Run Scorers in {season}",
    height=500
))

# --------------------
# Matches per Venue
# --------------------
venue_counts = (
    season_matches['venue']
    .value_counts()
    .reset_index()
    .rename(columns={'index': 'venue', 'venue': 'matches'})
)

#st.subheader(f"Matches per Venue - {season}")
#st.plotly_chart(px.bar(
 #   venue_counts,
 #   x="venue",
  #  y="matches",
   # color="matches",
    #color_continuous_scale="Viridis",
    #title="Matches per Venue",
    #height=500
#)) ###

# --------------------
# Win by Runs / Wickets
# --------------------
col1, col2 = st.columns(2)

with col1:
    win_by_runs = season_matches.groupby('winner')['win_by_runs'].sum().reset_index()
    st.plotly_chart(px.bar(
        win_by_runs,
        x="winner",
        y="win_by_runs",
        title="Total Runs Margin Wins",
        color="win_by_runs",
        color_continuous_scale="reds"
    ))

with col2:
    win_by_wickets = season_matches.groupby('winner')['win_by_wickets'].sum().reset_index()
    st.plotly_chart(px.bar(
        win_by_wickets,
        x="winner",
        y="win_by_wickets",
        title="Total Wickets Margin Wins",
        color="win_by_wickets",
        color_continuous_scale="greens"
    ))

# --------------------
# Footer
# --------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Pandas & Plotly")
