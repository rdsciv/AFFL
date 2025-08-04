import pandas as pd
from espn_api.football import League
import sqlite3
import time
import os

# Replace with your league ID
LEAGUE_ID = 51418

# Define the range of years to fetch data for
START_YEAR = 2014
END_YEAR = 2024

# Database file path (new location)
db_path = r'C:\Users\Ryan_\fantasy_football_analysis\espn_fantasy_football_new_db\espn_fantasy_football.db'

# --- Delete existing database file to ensure clean slate ---
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database file: {db_path}")

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS leagues (
    year INTEGER PRIMARY KEY,
    league_id INTEGER,
    league_name TEXT,
    num_teams INTEGER,
    scoring_type TEXT,
    draft_type TEXT,
    playoff_week_start INTEGER,
    reg_season_count INTEGER,
    trade_deadline TEXT,
    waiver_rule TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS members (
    year INTEGER,
    member_id TEXT,
    display_name TEXT,
    is_league_manager BOOLEAN,
    PRIMARY KEY (year, member_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS teams (
    year INTEGER,
    team_id INTEGER,
    team_name TEXT,
    owner_name TEXT,
    wins INTEGER,
    losses INTEGER,
    ties INTEGER,
    points_for REAL,
    points_against REAL,
    final_standing INTEGER,
    division_name TEXT,
    acquisitions INTEGER,
    drops INTEGER,
    trades INTEGER,
    waiver_rank INTEGER,
    acquisition_budget_spent REAL,
    PRIMARY KEY (year, team_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS draft_picks (
    year INTEGER,
    player_id INTEGER,
    player_name TEXT,
    team_id INTEGER,
    team_name TEXT,
    position TEXT,
    bid_amount REAL,
    round_num INTEGER,
    pick_num INTEGER,
    PRIMARY KEY (year, player_id, team_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS player_season_stats (
    year INTEGER,
    player_id INTEGER,
    player_name TEXT,
    position TEXT,
    pro_team TEXT,
    avg_draft_position REAL,
    percent_owned REAL,
    percent_rostered REAL,
    total_points REAL,
    total_receptions REAL,
    total_rushing_yards REAL,
    total_rushing_tds REAL,
    total_passing_yards REAL,
    total_passing_tds REAL,
    total_interceptions REAL,
    total_sacks REAL,
    total_tackles REAL,
    total_fumbles_recovered REAL,
    total_interceptions_returned_for_td REAL,
    PRIMARY KEY (year, player_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    year INTEGER,
    transaction_id TEXT,
    transaction_type TEXT,
    date TEXT,
    team_id INTEGER,
    team_name TEXT,
    player_id INTEGER,
    player_name TEXT,
    action_type TEXT,
    bid_amount REAL,
    PRIMARY KEY (year, transaction_id, player_id, action_type)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS matchups (
    year INTEGER,
    week INTEGER,
    home_team_id INTEGER,
    home_team_score REAL,
    away_team_id INTEGER,
    away_team_score REAL,
    winner_team_id INTEGER,
    PRIMARY KEY (year, week, home_team_id)
)
''')
conn.commit()

print(f"Connected to database: {db_path}")

for year in range(START_YEAR, END_YEAR + 1):
    print(f"\n--- Fetching data for {year} ---")
    try:
        league = League(league_id=LEAGUE_ID, year=year)

        if league and hasattr(league, 'settings') and hasattr(league.settings, 'name'):
            print(f"League Name: {league.settings.name} ({year})")
            
            # --- Leagues Data ---
            try:
                league_data = pd.DataFrame([{
                    'year': year,
                    'league_id': LEAGUE_ID,
                    'league_name': league.settings.name,
                    'num_teams': len(league.teams),
                    'scoring_type': getattr(league.settings, 'scoring_type', 'N/A'),
                    'draft_type': getattr(league.settings, 'draft_type', 'N/A'),
                    'playoff_week_start': getattr(league.settings, 'playoff_week_start', 0),
                    'reg_season_count': getattr(league.settings, 'reg_season_count', 0),
                    'trade_deadline': getattr(league.settings, 'trade_deadline', 'N/A'),
                    'waiver_rule': getattr(league.settings, 'waiver_rule', 'N/A'),
                }])
                league_data.to_sql('leagues', conn, if_exists='append', index=False)
                print("Leagues data saved.")
            except Exception as e:
                print(f"Error saving leagues data for {year}: {e}")

            # --- Members Data ---
            try:
                members_data = []
                if hasattr(league, 'members') and league.members:
                    for member in league.members:
                        # Ensure member is a dictionary before accessing keys
                        if isinstance(member, dict):
                            members_data.append({
                                'year': year,
                                'member_id': member.get('id', 'N/A'),
                                'display_name': member.get('displayName', 'N/A'),
                                'is_league_manager': member.get('isLeagueManager', False),
                            })
                        else:
                            print(f"Skipping non-dict member object for {year}: {member}")
                df_members = pd.DataFrame(members_data)
                if not df_members.empty:
                    df_members.to_sql('members', conn, if_exists='append', index=False)
                    print("Members data saved.")
                else:
                    print("No members data found.")
            except Exception as e:
                print(f"Error saving members data for {year}: {e}")

            # --- Teams Data ---
            try:
                teams_data = []
                for team in league.teams:
                    owner_name = team.owners[0]['displayName'] if team.owners else 'N/A'
                    teams_data.append({
                        'year': year,
                        'team_id': getattr(team, 'team_id', 0),
                        'team_name': getattr(team, 'team_name', 'N/A'),
                        'owner_name': owner_name,
                        'wins': getattr(team, 'wins', 0),
                        'losses': getattr(team, 'losses', 0),
                        'ties': getattr(team, 'ties', 0),
                        'points_for': getattr(team, 'points_for', 0.0),
                        'points_against': getattr(team, 'points_against', 0.0),
                        'final_standing': getattr(team, 'final_standing', 0),
                        'division_name': getattr(team, 'division_name', 'N/A'),
                        'acquisitions': getattr(team, 'acquisitions', 0),
                        'drops': getattr(team, 'drops', 0),
                        'trades': getattr(team, 'trades', 0),
                        'waiver_rank': getattr(team, 'waiver_rank', 0),
                        'acquisition_budget_spent': getattr(team, 'acquisition_budget_spent', 0.0),
                })
                df_teams = pd.DataFrame(teams_data)
                df_teams.to_sql('teams', conn, if_exists='append', index=False)
                print("Teams data saved.")
            except Exception as e:
                print(f"Error saving teams data for {year}: {e}")

            # --- Draft Picks Data ---
            try:
                draft_picks_data = []
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
                        
                        position = 'N/A' # Position remains N/A for now

                        draft_picks_data.append({
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
                    df_draft_picks = pd.DataFrame(draft_picks_data)
                    df_draft_picks.to_sql('draft_picks', conn, if_exists='append', index=False)
                    print("Draft picks data saved.")
                else:
                    print("No draft data found.")
            except Exception as e:
                print(f"Error saving draft picks data for {year}: {e}")

            # --- Player Season Stats Data ---
            try:
                player_season_stats_data = []
                if hasattr(league, 'player_map') and league.player_map:
                    for player_id, player_obj in league.player_map.items():
                        position = getattr(player_obj, 'position', 'N/A')
                        if position == 'N/A': # Try posRank if position is N/A
                            position = getattr(player_obj, 'posRank', 'N/A')
                        if position == 'N/A' and hasattr(player_obj, 'defaultPositionId'):
                            position_map_id = {
                                1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'
                            }
                            position = position_map_id.get(player_obj.defaultPositionId, 'N/A')

                        # Safely extract season totals if available and is a dictionary
                        total_stats = {}
                        if hasattr(player_obj, 'stats') and isinstance(player_obj.stats, dict):
                            total_stats = player_obj.stats.get(str(year), {}).get('total', {})

                        player_season_stats_data.append({
                            'year': year,
                            'player_id': player_id,
                            'player_name': getattr(player_obj, 'name', 'N/A'),
                            'position': position,
                            'pro_team': getattr(player_obj, 'proTeam', 'N/A'),
                            'avg_draft_position': getattr(player_obj, 'average_draft_position', 0.0),
                            'percent_owned': getattr(player_obj, 'percent_owned', 0.0),
                            'percent_rostered': getattr(player_obj, 'percent_rostered', 0.0),
                            'total_points': total_stats.get('points', 0.0),
                            'total_receptions': total_stats.get('receptions', 0.0),
                            'total_rushing_yards': total_stats.get('rushingYards', 0.0),
                            'total_rushing_tds': total_stats.get('rushingTouchdowns', 0.0),
                            'total_passing_yards': total_stats.get('passingYards', 0.0),
                            'total_passing_tds': total_stats.get('passingTouchdowns', 0.0),
                            'total_interceptions': total_stats.get('interceptions', 0.0),
                            'total_sacks': total_stats.get('sacks', 0.0),
                            'total_tackles': total_stats.get('tackles', 0.0),
                            'total_fumbles_recovered': total_stats.get('fumblesRecovered', 0.0),
                            'total_interceptions_returned_for_td': total_stats.get('interceptionReturnTouchdowns', 0.0),
                        })
                df_player_season_stats = pd.DataFrame(player_season_stats_data)
                if not df_player_season_stats.empty:
                    df_player_season_stats.to_sql('player_season_stats', conn, if_exists='append', index=False)
                    print("Player season stats data saved.")
                else:
                    print("No player season stats data found.")
            except Exception as e:
                print(f"Error saving player season stats data for {year}: {e}")

            # --- Transactions Data ---
            try:
                transactions_data = []
                if hasattr(league, 'recent_activity') and league.recent_activity:
                    recent_activity = league.recent_activity()
                    for transaction in recent_activity:
                        # Safely get transaction attributes
                        transaction_id = getattr(transaction, 'transaction_id', 'N/A')
                        transaction_type = getattr(transaction, 'type', 'N/A')
                        transaction_date = getattr(transaction, 'date', None)
                        formatted_date = transaction_date.strftime('%Y-%m-%d %H:%M:%S') if transaction_date else 'N/A'

                        # Safely get team info
                        team_id = getattr(transaction.team, 'team_id', 0) if transaction.team else 0
                        team_name = getattr(transaction.team, 'team_name', 'N/A') if transaction.team else 'N/A',

                        # Safely iterate through actions
                        if hasattr(transaction, 'actions') and transaction.actions:
                            for action in transaction.actions:
                                transactions_data.append({
                                    'year': year,
                                    'transaction_id': transaction_id,
                                    'transaction_type': transaction_type,
                                    'date': formatted_date,
                                    'team_id': team_id,
                                    'team_name': team_name,
                                    'player_id': getattr(action.player, 'playerId', 0) if hasattr(action, 'player') and action.player else 0,
                                    'player_name': getattr(action.player, 'name', 'N/A') if hasattr(action, 'player') and action.player else 'N/A',
                                    'action_type': getattr(action, 'type', 'N/A'),
                                    'bid_amount': getattr(action, 'bid_amount', 0.0),
                                })
                df_transactions = pd.DataFrame(transactions_data)
                if not df_transactions.empty:
                    df_transactions.to_sql('transactions', conn, if_exists='append', index=False)
                    print("Transactions data saved.")
                else:
                    print("No transactions data found.")
            except Exception as e:
                print(f"Error saving transactions data for {year}: {e}")

            # --- Matchups Data ---
            try:
                matchups_data = []
                for week in range(1, 18): # Assuming a max of 17 weeks for fantasy regular season
                    scoreboard = league.scoreboard(week=week)
                    if not scoreboard: # Break if no more matchups for the year
                        break
                    for matchup in scoreboard:
                        # Safely get home and away team objects
                        home_team_obj = getattr(matchup, 'home_team', None)
                        away_team_obj = getattr(matchup, 'away_team', None)

                        home_team_id = getattr(home_team_obj, 'team_id', 0) if home_team_obj else 0
                        away_team_id = getattr(away_team_obj, 'team_id', 0) if away_team_obj else 0

                        winner_team_id = None
                        if getattr(matchup, 'winner', None) == 'home':
                            winner_team_id = home_team_id
                        elif getattr(matchup, 'winner', None) == 'away':
                            winner_team_id = away_team_id

                        matchups_data.append({
                            'year': year,
                            'week': week,
                            'home_team_id': home_team_id,
                            'home_team_score': getattr(matchup, 'home_score', 0.0),
                            'away_team_id': away_team_id,
                            'away_team_score': getattr(matchup, 'away_score', 0.0),
                            'winner_team_id': winner_team_id,
                        })
                df_matchups = pd.DataFrame(matchups_data)
                if not df_matchups.empty:
                    df_matchups.to_sql('matchups', conn, if_exists='append', index=False)
                    print("Matchups data saved.")
                else:
                    print(f"No matchup data found for {year}.")
            except Exception as e:
                print(f"Error saving matchups data for {year}: {e}")

        else:
            print(f"Could not retrieve league settings for {year}. Skipping year.")

    except Exception as e:
        print(f"An error occurred for {year}: {e}")
        print(f"Skipping year {year}. Please ensure your league ID is correct. If it's a private league, you may need to provide ESPN_S2 and SWID cookies.")

    time.sleep(1) # Add a small delay between years to avoid rate limiting

conn.close()
print(f"\nData scraping complete. All available data saved to {db_path}")