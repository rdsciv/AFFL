import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Database file path
db_path = r'C:\Users\Ryan_\fantasy_football_analysis\espn_fantasy_football.db'

print(f"Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)

# Load data from database
df_draft_picks = pd.read_sql_query("SELECT * FROM draft_picks", conn)
df_teams = pd.read_sql_query("SELECT * FROM teams", conn)

conn.close()
print("Data loaded successfully.")

# Filter for East division teams
east_division_teams = df_teams[df_teams['division_name'] == 'East']

# Merge draft picks with team information to get division data
df_merged = pd.merge(
    df_draft_picks,
    east_division_teams[['team_id', 'team_name', 'division_name']],
    on=['team_id', 'team_name'],
    how='inner'
)

# Filter out 'N/A' positions for this analysis
df_filtered = df_merged[df_merged['position'] != 'N/A']

# Calculate spending by team and position
spending_by_team_position = df_filtered.groupby(['team_name', 'position'])['bid_amount'].sum().unstack(fill_value=0)

print("\n--- Spending by East Division Team and Position ---")
print(spending_by_team_position)

# Create a beautiful stacked bar chart
plt.figure(figsize=(15, 8))
spending_by_team_position.plot(kind='bar', stacked=True, colormap='viridis', ax=plt.gca())

plt.title('East Division Team Spending by Position (2020-2024)', fontsize=18)
plt.xlabel('Team Name', fontsize=14)
plt.ylabel('Total Bid Amount', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Position', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

output_chart_path = r'C:\Users\Ryan_\fantasy_football_analysis\east_division_spending_by_position.png'
plt.savefig(output_chart_path)
plt.close()

print(f"\nChart saved to {output_chart_path}")
print("Analysis complete.")
