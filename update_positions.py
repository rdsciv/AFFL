import pandas as pd
import sqlite3
from espn_api.football import League

# Database file path
db_path = r'C:\Users\Ryan_\fantasy_football_analysis\espn_fantasy_football.db'

# Define the range of years to fetch data for
START_YEAR = 2014
END_YEAR = 2024

print(f"Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)

all_draft_picks_data = []

for year in range(START_YEAR, END_YEAR + 1):
    print(f"\n--- Processing data for {year} ---")
    try:
        league = League(league_id=51418, year=year)

        if league and hasattr(league, 'settings') and hasattr(league.settings, 'name'):
            print(f"League Name: {league.settings.name} ({year})")
            
            # Create a player-position mapping for the current year
            player_position_map_current_year = {}
            if hasattr(league, 'player_map'):
                for player_id, player_obj in league.player_map.items():
                    position = 'N/A'
                    if hasattr(player_obj, 'position') and player_obj.position:
                        position = player_obj.position
                    elif hasattr(player_obj, 'posRank') and player_obj.posRank:
                        position = player_obj.posRank
                    elif hasattr(player_obj, 'defaultPositionId') and player_obj.defaultPositionId:
                        position_map_id = {
                            1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'
                        }
                        position = position_map_id.get(player_obj.defaultPositionId, 'N/A')
                    player_position_map_current_year[player_id] = position

            draft_picks = []
            if hasattr(league, 'draft'):
                if callable(league.draft):
                    draft_picks = league.draft()
                else:
                    draft_picks = league.draft

            if draft_picks:
                for pick in draft_picks:
                    player_name = getattr(pick, 'playerName', 'N/A')
                    team_name = getattr(pick.team, 'team_name', 'N/A')
                    bid_amount = getattr(pick, 'bid_amount', 0.0)
                    
                    position = player_position_map_current_year.get(getattr(pick, 'playerId', 0), 'N/A')

                    all_draft_picks_data.append({
                        'year': year,
                        'player_id': getattr(pick, 'playerId', 0),
                        'player_name': player_name,
                        'team_id': getattr(pick.team, 'team_id', 0),
                        'team_name': team_name,
                        'position': position,
                        'bid_amount': bid_amount,
                        'round_num': getattr(pick, 'round_num', 0),
                        'pick_num': getattr(pick, 'pick_num', 0),
                    })
            else:
                print(f"No draft data found for {year}.")
        else:
            print(f"Could not retrieve league settings for {year}. Skipping year.")

    except Exception as e:
        print(f"An error occurred for {year}: {e}")
        print(f"Skipping year {year}. Please ensure your league ID is correct. If it's a private league, you may need to provide ESPN_S2 and SWID cookies.")

# Create DataFrame from all collected draft picks
df_all_draft_picks = pd.DataFrame(all_draft_picks_data)

# Overwrite the existing draft_picks table in the database
print("\nOverwriting draft_picks table in the database...")
df_all_draft_picks.to_sql('draft_picks', conn, if_exists='replace', index=False)

conn.close()
print("Database updated successfully with player positions.")

print("\n--- Updated Draft Picks Data Head (from DB) ---")
conn = sqlite3.connect(db_path)
df_updated_draft_picks = pd.read_sql_query("SELECT * FROM draft_picks", conn)
print(df_updated_draft_picks.head())
print("\n--- Updated Draft Picks Position Value Counts (from DB) ---")
print(df_updated_draft_picks['position'].value_counts(dropna=False))
conn.close()