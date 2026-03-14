import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import numpy as np 
import streamlit as st 
#step 1  ; load the dataset 
df1 = pd.read_csv("c:\\Users\\ISHAAN\\Downloads\\matches.csv")
df2 = pd.read_csv("c:\\Users\\ISHAAN\\Downloads\\deliveries.csv")
sns.set_style('whitegrid')
#top run scorers
grouped_data = df2.groupby('batsman')      #group the data by 'batsman' column data ws scattered so i grouped all the numbers and put them in one container
total_runs = grouped_data['batsman_runs'].sum()  #summed them
top_scorers = total_runs.sort_values(ascending=False) #sorted the data in descending order to get the top scorers at the top
print(top_scorers.head(10))                       #print the top 10 run scorers
# Prepare horizontal bar chart for top 10 scorers with a color palette
top10 = top_scorers.head(10)
top10 = top10.iloc[::1]  # reverse so highest scorer appears at top
sns.barplot(x=top10.values, y=top10.index, palette=sns.color_palette("viridis", len(top10)))
plt.title('Top 10 Run Scorers in IPL')
plt.xlabel('Total Runs Scored')
plt.ylabel('Batsman')
plt.tight_layout() # Ensures labels aren't cut off
plt.savefig('top_scorers_plot.png')
plt.show()
#Color Palettes: Using palettes like viridis or magma isn't just for looks—they are designed to be "perceptually uniform," meaning the difference in color accurately represents the difference in data.
#Horizontal vs Vertical: If you have many categories (like 10-15 players), use Horizontal bars (y=PlayerName). If you have few categories (like 3-5 teams), use Vertical bars.
#the strike rate of the top 10 run scorers
grouped_data = df2.groupby('batsman') #group the data by 'batsman' column data ws scattered so i grouped all the numbers and put them in one container
strike_rates = grouped_data['batsman_runs'].sum() / grouped_data['batsman_runs'].count() * 100 # made a  strike rate formula 
top_strike_rates = strike_rates.sort_values(ascending=False) #sorted the data in descending order to get the top strike rates at the top
print(top_strike_rates.head(10)) #print the top 10 strike rates 
top10_strike = top_strike_rates.head(10)
# convert to DataFrame for seaborn
top10_strike_df = top10_strike.reset_index() #turns the Series into a DataFrame and makes 'batsman' a column instead of an index
top10_strike_df.columns = ['batsman', 'strike_rate']
plt.figure(figsize=(8,6))
sns.barplot(data=top10_strike_df, x='batsman', y='strike_rate', palette='magma')
plt.title('Top 10 Strike Rates in IPL History')
plt.xlabel('Batsman')
plt.ylabel('Strike Rate')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_strike_rates_plot.png')
plt.show()

# -------------------------
# Additional visualizations
# -------------------------
# compute strike-rate per innings (exclude wides for balls faced)
try:
	innings = (
		df2[df2['wide_runs'] == 0]
		.groupby(['match_id', 'batsman'])
		.agg(runs=('batsman_runs', 'sum'), balls=('batsman_runs', 'count'))
		.reset_index()
	)
	innings['strike_rate'] = innings['runs'] / innings['balls'] * 100

	# choose top batsmen to avoid overcrowding
	top_bats = top_scorers.head(8).index.tolist()

	# 1) Boxplot + stripplot: per-innings spread for top batsmen
	plt.figure(figsize=(10,6))
	sns.boxplot(data=innings[innings['batsman'].isin(top_bats)], x='batsman', y='strike_rate', order=top_bats)
	sns.stripplot(data=innings[innings['batsman'].isin(top_bats)], x='batsman', y='strike_rate', order=top_bats, color='k', size=3, alpha=0.5)
	plt.title('Per-innings Strike Rate Distribution (Top batsmen)')
	plt.xlabel('Batsman')
	plt.ylabel('Strike Rate')
	plt.xticks(rotation=45, ha='right')
	plt.tight_layout()
	plt.savefig('strike_rate_box_strip.png')
	plt.show()

	# 2) Scatter: strike rate vs balls faced (use innings-level points)
	plt.figure(figsize=(8,6))
	sample = innings[innings['batsman'].isin(top_bats)]
	sns.scatterplot(data=sample, x='balls', y='strike_rate', hue='batsman', alpha=0.7)
	plt.title('Strike Rate vs Balls Faced (per-innings)')
	plt.xlabel('Balls Faced')
	plt.ylabel('Strike Rate')
	plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
	plt.tight_layout()
	plt.savefig('strike_rate_scatter.png')
	plt.show()

	# 3) Heatmap: batsman x season (if season available in matches)
	if 'match_id' in df2.columns and 'id' in df1.columns and 'season' in df1.columns:
		merged = innings.merge(df1[['id', 'season']], left_on='match_id', right_on='id', how='left')
		pivot = (
			merged[merged['batsman'].isin(top_bats)]
			.pivot_table(index='batsman', columns='season', values='strike_rate', aggfunc='mean')
		)
		plt.figure(figsize=(10,6))
		sns.heatmap(pivot, cmap='magma', annot=True, fmt='.1f', linewidths=.5)
		plt.title('Average Strike Rate by Season (Top batsmen)')
		plt.tight_layout()
		plt.savefig('strike_rate_heatmap.png')
		plt.show()

	# 4) Histogram / KDE: distribution of per-innings strike rates
	plt.figure(figsize=(8,5))
	sns.histplot(innings['strike_rate'], kde=True)
	plt.title('Distribution of Per-innings Strike Rates')
	plt.xlabel('Strike Rate')
	plt.tight_layout()
	plt.savefig('strike_rate_distribution.png')
	plt.show()
except Exception as e:
	print('Could not build additional visualizations:', e)
             
#best wicket takers
#not all the wickets have been taken by only bowlers so we will not consider the wickets tsken by  the feilders and the run outs
# 1. Define the list of dismissals credited to the bowler
# This list includes the types of dismissals that are typically credited to the bowler. We will use this list to filter our dataset and focus only on the rows w""here the dismissal_kind matches one of these criteria.
bowler_stats_criteria = ['bowled', 'lbw', 'caught', 'stumped', 'caught and bowled', 'hit wicket']

# 2. Filter the datasheet
# This says: "Keep the row only if the dismissal_kind is in my list"
bowler_wickets_df = df2[df2['dismissal_kind'].isin(bowler_stats_criteria)]#Since we want to count only what goes on the bowler's "scorecard," we use the .isin() syntax to include the catch.
#grop this filterred data by the 'bowler' column and count the number of wickets taken by each bowler

bowler_wickets_count = bowler_wickets_df.groupby('bowler')['dismissal_kind'].count() #group the data by 'bowler' column and count the number of wickets taken by each bowler
#sort the bowlers by the number of wickets taken in descending order and print the top 10 wicket takers 
top_wicket_takers = bowler_wickets_count.sort_values(ascending=False)
print(top_wicket_takers.head(10))
# show only top 10 wicket takers as a horizontal bar (faster and clearer)
top10_bowlers = top_wicket_takers.head(10)
plt.figure(figsize=(8,6))
sns.barplot(x=top10_bowlers.values, y=top10_bowlers.index, palette='magma')
plt.title('Top 10 Wicket Takers in IPL History')
plt.xlabel('Wickets')
plt.ylabel('Bowler')
plt.tight_layout()
plt.savefig('top_wicket_takers_plot.png')
plt.show()
# showing the economy of all the top 10  wicket takers 
#Economy Rate = {Total\ Runs\ Conceded}\{Total\ Overs\ Bowled}
# compute runs conceded per ball (exclude byes and legbyes) and sum per bowler
df2['runs_conceded_ball'] = df2['total_runs'] - df2['bye_runs'] - df2['legbye_runs']
runs_conceded = df2.groupby('bowler')['runs_conceded_ball'].sum()

# count legal deliveries per bowler (exclude wides and no-balls)
legal_balls = df2[(df2['wide_runs'] == 0) & (df2['noball_runs'] == 0)].groupby('bowler').size()

# align indices and avoid missing bowlers
bowlers = runs_conceded.index.union(legal_balls.index)
runs_conceded = runs_conceded.reindex(bowlers, fill_value=0)
legal_balls = legal_balls.reindex(bowlers, fill_value=0)

# convert balls -> overs and compute economy safely (avoid division by zero)
overs = legal_balls / 6
economy = pd.Series(index=bowlers, dtype=float)
valid = overs > 0
economy[valid] = runs_conceded[valid] / overs[valid]

# drop bowlers with no legal deliveries
economy = economy.dropna()

top10_worst = economy.sort_values(ascending=False).head(10)  # worst
top10_best  = economy.sort_values(ascending=True).head(10)   # best
print('Top 10 worst economy rates (higher is worse):')
print(top10_worst)
print('\nTop 10 best economy rates (lower is better):')
print(top10_best)

# Plot best and worst economy rates
if not top10_best.empty:
	plt.figure(figsize=(8,6))
	sns.barplot(x=top10_best.values, y=top10_best.index, palette='Blues_r')
	plt.title('Top 10 Best Economy Rates')
	plt.xlabel('Economy Rate')
	plt.ylabel('Bowler')
	plt.tight_layout()
	plt.savefig('top10_best_economy.png')
	plt.show()

if not top10_worst.empty:
	plt.figure(figsize=(8,6))
	sns.barplot(x=top10_worst.values, y=top10_worst.index, palette='Reds')
	plt.title('Top 10 Worst Economy Rates')
	plt.xlabel('Economy Rate')
	plt.ylabel('Bowler')
	plt.tight_layout()
	plt.savefig('top10_worst_economy.png')
	plt.show()
#reset_index() does: it converts the Series index into a column and returns a DataFrame (Seaborn works best with DataFrames).
