from espn_api.football import League
import pandas as pd

# Replace with your league ID
LEAGUE_ID = 51418

# Define the range of years to fetch data for
START_YEAR = 2014
END_YEAR = 2024

# If your league is private, you'll need to provide ESPN_S2 and SWID cookies.
# You can get these by logging into ESPN fantasy football in your browser,
# opening developer tools (F12), going to the Network tab, and inspecting
# a request to `fantasy.espn.com`. Look for the `Cookie` header.
# For public leagues, these are not necessary.
# ESPN_S2 = 'YOUR_ESPN_S2_COOKIE'
# SWID = '{YOUR_SWID_COOKIE}'

all_auction_data = []

for year in range(START_YEAR, END_YEAR + 1):
    print(f"\n--- Fetching data for {year} ---")
    try:
        # For public leagues:
        league = League(league_id=LEAGUE_ID, year=year)

        # For private leagues (uncomment and provide your cookies):
        # league = League(league_id=LELEAGUE_ID, year=year, espn_s2=ESPN_S2, swid=SWID)

        if league and hasattr(league, 'settings') and hasattr(league.settings, 'name'):
            print(f"League Name: {league.settings.name} ({year})")
            
            draft_picks = []
            if hasattr(league, 'draft'):
                if callable(league.draft):
                    draft_picks = league.draft()
                else:
                    draft_picks = league.draft

            if draft_picks:
                print("Draft data found! Extracting auction values...")
                for pick in draft_picks:
                    try:
                        player_name = pick.playerName
                        team_name = pick.team.team_name
                        bid_amount = pick.bid_amount
                        
                        # Attempt to get player position directly from pick.player.position
                        position = 'N/A'
                        if hasattr(pick, 'player') and hasattr(pick.player, 'position'):
                            position = pick.player.position
                        
                        all_auction_data.append({
                            'Year': year,
                            'Player': player_name,
                            'Team': team_name,
                            'Position': position,
                            'Bid_Amount': bid_amount
                        })
                    except Exception as pick_e:
                        print(f"Error processing pick for {year}: {pick_e} - Pick details: {pick}")
            else:
                print(f"No draft data found for {year}.")
        else:
            print(f"Could not retrieve league settings for {year}. Skipping year.")

    except Exception as e:
        print(f"An error occurred for {year}: {e}")
        print(f"Skipping year {year}. Please ensure your league ID is correct. If it's a private league, you may need to provide ESPN_S2 and SWID cookies.")

# Combine all data into a single DataFrame
df_all_auction = pd.DataFrame(all_auction_data)

# Save the combined DataFrame to a CSV
output_csv_path = rf'C:\Users\Ryan_\fantasy_football_analysis\espn_auction_values_{START_YEAR}_{END_YEAR}.csv'
df_all_auction.to_csv(output_csv_path, index=False)
print(f"\nAll auction values extracted and saved to {output_csv_path}")

print("\n--- Combined Auction Values Analysis ---")
print(df_all_auction.head())
print("\nSummary Statistics:")
print(df_all_auction.describe())

# You can now perform more in-depth analysis and visualizations on df_all_auction