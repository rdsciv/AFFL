import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined auction data
file_path = r'C:\Users\Ryan_\fantasy_football_analysis\espn_auction_values_2014_2024.csv'
df_auction = pd.read_csv(file_path)

# --- Data Cleaning and Preparation ---
# Ensure 'Bid_Amount' is numeric, coercing errors will turn non-numeric into NaN
df_auction['Bid_Amount'] = pd.to_numeric(df_auction['Bid_Amount'], errors='coerce')
# Drop rows where Bid_Amount is NaN (e.g., if a player was not drafted in an auction)
df_auction.dropna(subset=['Bid_Amount'], inplace=True)

# Convert 'Bid_Amount' to integer for cleaner display
df_auction['Bid_Amount'] = df_auction['Bid_Amount'].astype(int)

# Drop the 'Position' column as it's not populated
df_auction.drop(columns=['Position'], inplace=True)

print("\n--- Cleaned Data Head ---")
print(df_auction.head())
print("\n--- Cleaned Data Info ---")
print(df_auction.info())

# --- Analysis: Overall Average Bid Amount Over Years ---
# Calculate overall average bid amount per year
avg_bid_overall_year = df_auction.groupby(['Year'])['Bid_Amount'].mean()

print("\n--- Overall Average Bid Amount by Year ---")
print(avg_bid_overall_year)

# --- Visualizations ---

# 1. Line Plot: Overall Average Bid Amount Over Years
plt.figure(figsize=(12, 7))
avg_bid_overall_year.plot(kind='line', marker='o')
plt.title('Overall Average Auction Bid Amount Over Years', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Bid Amount', fontsize=12)
plt.xticks(avg_bid_overall_year.index)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(r'C:\Users\Ryan_\fantasy_football_analysis\overall_avg_bid_over_years.png')
plt.close()

# 2. Bar Chart: Top Players by Average Bid Amount (across all years, regardless of position)
# Calculate average bid amount per player across all years they were drafted
avg_bid_per_player = df_auction.groupby(['Player'])['Bid_Amount'].mean().reset_index()
# Sort by average bid amount and get top N players
top_n_players = avg_bid_per_player.sort_values(by='Bid_Amount', ascending=False).head(20)

plt.figure(figsize=(14, 8))
sns.barplot(data=top_n_players, x='Bid_Amount', y='Player', palette='coolwarm')
plt.title('Top 20 Players by Average Auction Bid Amount (2020-2024)', fontsize=16)
plt.xlabel('Average Bid Amount', fontsize=12)
plt.ylabel('Player', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(r'C:\Users\Ryan_\fantasy_football_analysis\top_players_by_avg_bid_no_position.png')
plt.close()

print("Analysis and visualizations complete. Check the fantasy_football_analysis directory for output files.")