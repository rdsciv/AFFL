
import pandas as pd
import numpy as np

# Define players and positions
players = {
    "Patrick Mahomes": "QB", "Travis Kelce": "TE", "Tyreek Hill": "WR",
    "Christian McCaffrey": "RB", "Cooper Kupp": "WR", "Josh Allen": "QB",
    "Jonathan Taylor": "RB", "Justin Jefferson": "WR", "Mark Andrews": "TE",
    "Austin Ekeler": "RB", "Stefon Diggs": "WR", "Lamar Jackson": "QB"
}

teams = ["KC", "SF", "LAR", "BUF", "IND", "MIN", "BAL", "LAC"]

# Generate data for 10 weeks
data = []
for week in range(1, 11):
    for player, position in players.items():
        team = np.random.choice(teams)
        points = round(np.random.uniform(5, 30), 2)  # Random points between 5 and 30
        touchdowns = np.random.randint(0, 4)  # Random touchdowns between 0 and 3
        yards = np.random.randint(30, 300)  # Random yards between 30 and 300
        data.append([player, team, position, week, points, touchdowns, yards])

df = pd.DataFrame(data, columns=["Player", "Team", "Position", "Week", "Points", "Touchdowns", "Yards"])

# Save to CSV
output_path = r'C:\Users\Ryan_\fantasy_football_analysis\fantasy_football_data.csv'
df.to_csv(output_path, index=False)

print(f"Dummy data generated and saved to {output_path}")
