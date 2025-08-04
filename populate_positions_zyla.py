import pandas as pd
import sqlite3
# Removed requests and time imports as Zyla API calls are skipped

# Database file path
db_path = r'C:\Users\Ryan_\fantasy_football_analysis\espn_fantasy_football.db'
ff_data_csv_path = r'C:\Users\Ryan_\fantasy_football_analysis\fantasy_football_data.csv'

print(f"Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)

print(f"Loading draft_picks table from {db_path}")
df_draft_picks = pd.read_sql_query("SELECT * FROM draft_picks", conn)

print(f"Loading fantasy_football_data.csv from {ff_data_csv_path}")
df_ff_data = pd.read_csv(ff_data_csv_path)

# Create a player-position mapping from fantasy_football_data.csv
# Take the first unique position for each player if they appear multiple times
player_position_map = df_ff_data.drop_duplicates(subset=['Player'])[['Player', 'Position']].set_index('Player')['Position'].to_dict()

print("Updating positions in draft_picks DataFrame using fantasy_football_data.csv...")
# Apply the mapping to the 'position' column where it's 'N/A'
def update_position_from_csv(row):
    if row['position'] == 'N/A':
        return player_position_map.get(row['player_name'], 'N/A')
    return row['position']

df_draft_picks['position'] = df_draft_picks.apply(update_position_from_csv, axis=1)

# Overwrite the existing draft_picks table in the database
print("\nOverwriting draft_picks table in the database with updated positions...")
df_draft_picks.to_sql('draft_picks', conn, if_exists='replace', index=False)

conn.close()
print("Database updated successfully with player positions from fantasy_football_data.csv.")

print("\n--- Updated Draft Picks Data Head (from DB) ---")
conn = sqlite3.connect(db_path)
df_updated_draft_picks = pd.read_sql_query("SELECT * FROM draft_picks", conn)
print(df_updated_draft_picks.head())
print("\n--- Updated Draft Picks Position Value Counts (from DB) ---")
print(df_updated_draft_picks['position'].value_counts(dropna=False))
conn.close()