# ipl-dashboard
a mini project on ipl analysing using python library 
# ============================
# 1. Import Required Libraries
# ============================
# Purpose: Load all tools needed for data handling, visualization, and dashboard building.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# ============================
# 2. Load Datasets
# ============================
# Purpose: Read IPL data into Pandas DataFrames for analysis.
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# ============================
# 3. Basic Exploration
# ============================
# Purpose: Understand the structure of the data before analysis.
st.write("Matches Dataset Preview:", matches.head())
st.write("Deliveries Dataset Preview:", deliveries.head())
st.write("Matches Shape:", matches.shape)
st.write("Deliveries Shape:", deliveries.shape)

# ============================
# 4. Season-Level Analysis
# ============================
# Purpose: See how IPL evolved season by season.
season_counts = matches['season'].value_counts()
st.subheader("Number of Matches per Season")
st.bar_chart(season_counts)

champions = matches.dropna(subset=['winner']).groupby('season')['winner'].last()
st.subheader("Season-wise Champions")
st.write(champions)

# ============================
# 5. Team Performance Analysis
# ============================
# Purpose: Identify strongest teams and their winning patterns.
team_wins = matches['winner'].value_counts()
st.subheader("Most Successful Teams")
st.bar_chart(team_wins)

toss_decision = matches['toss_decision'].value_counts()
st.subheader("Toss Decision Trends")
st.bar_chart(toss_decision)

# ============================
# 6. Player Performance Analysis
# ============================
# Purpose: Highlight top players across seasons.
pom_counts = matches['player_of_match'].value_counts().head(10)
st.subheader("Top Player of the Match Winners")
st.bar_chart(pom_counts)

batsman_runs = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
st.subheader("Top Run Scorers")
st.bar_chart(batsman_runs)

bowler_wickets = deliveries[deliveries['dismissal_kind'].notnull()].groupby('bowler').size().sort_values(ascending=False).head(10)
st.subheader("Top Wicket Takers")
st.bar_chart(bowler_wickets)

# ============================
# 7. Venue Analysis
# ============================
# Purpose: Understand which stadiums host most matches and scoring trends.
venue_counts = matches['venue'].value_counts().head(10)
st.subheader("Matches per Venue")
st.bar_chart(venue_counts)

venue_runs = deliveries.groupby('venue')['total_runs'].mean().sort_values(ascending=False).head(10)
st.subheader("Average Runs per Venue")
st.bar_chart(venue_runs)

# ============================
# 8. Advanced Metrics
# ============================
# Purpose: Calculate strike rates and economy rates for deeper insights.
batsman_stats = deliveries.groupby('batsman').agg({'batsman_runs':'sum','ball':'count'})
batsman_stats['strike_rate'] = batsman_stats['batsman_runs'] / batsman_stats['ball'] * 100
top_sr = batsman_stats.sort_values('strike_rate', ascending=False).head(10)
st.subheader("Top Strike Rates")
st.write(top_sr)

bowler_stats = deliveries.groupby('bowler').agg({'total_runs':'sum','ball':'count'})
bowler_stats['overs'] = bowler_stats['ball'] / 6
bowler_stats['economy'] = bowler_stats['total_runs'] / bowler_stats['overs']
top_economy = bowler_stats.sort_values('economy').head(10)
st.subheader("Best Economy Rates")
st.write(top_economy)

# ============================
# 9. Streamlit Dashboard Layout
# ============================
# Purpose: Add interactivity with filters for season and team.
st.title("IPL Dashboard")

st.sidebar.title("Filters")
season = st.sidebar.selectbox("Select Season", matches['season'].unique())
team = st.sidebar.selectbox("Select Team", matches['team1'].unique())

filtered_matches = matches[(matches['season'] == season) & ((matches['team1'] == team) | (matches['team2'] == team))]
st.subheader(f"Performance of {team} in {season}")
team_wins = filtered_matches['winner'].value_counts()
st.bar_chart(team_wins)
- Step 1–2: Import libraries and load datasets → foundation of project.
- Step 3: Basic exploration → sanity check of data.
- Step 4: Season analysis → trends across years.
- Step 5: Team analysis → strongest teams, toss impact.
- Step 6: Player analysis → top performers (runs, wickets, awards).
- Step 7: Venue analysis → stadium impact on matches.
- Step 8: Advanced metrics → strike rate, economy rate for deeper cricket insights.
- Step 9: Streamlit layout → interactive filters for user-driven exploration.
