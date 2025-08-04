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

# --- Calculate Total Spending Per Team (including N/A positions) ---
# Merge draft picks with team names for easier grouping
df_merged_total = pd.merge(
    df_draft_picks,
    df_teams[['team_id', 'team_name']],
    on=['team_id', 'team_name'],
    how='inner'
)

total_spending_per_team = df_merged_total.groupby('team_name')['bid_amount'].sum().reset_index()
print("\n--- Total Spending Per Team (All Players) ---")
print(total_spending_per_team)

# --- Calculate Spending by Known Position Per Team ---
# Filter out 'N/A' positions for this specific positional breakdown
df_known_positions = df_merged_total[df_merged_total['position'] != 'N/A']

# Calculate spending by team and known position
spending_by_team_known_position = df_known_positions.groupby(['team_name', 'position'])['bid_amount'].sum().unstack(fill_value=0)

print("\n--- Spending by Team and Known Position ---")
print(spending_by_team_known_position)

# --- Create a Beautiful Stacked Bar Chart for All Teams ---
plt.figure(figsize=(18, 10))
spending_by_team_known_position.plot(kind='bar', stacked=True, colormap='viridis', ax=plt.gca())

plt.title('Team Spending by Position (All Teams, 2020-2024)', fontsize=20)
plt.xlabel('Team Name', fontsize=16)
plt.ylabel('Total Bid Amount', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='Position', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

output_chart_path = r'C:\Users\Ryan_\fantasy_football_analysis\all_team_spending_by_position.png'
plt.savefig(output_chart_path)
plt.close()

print(f"\nChart saved to {output_chart_path}")
print("Analysis complete.")
