import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
file_path = r'C:\Users\Ryan_\fantasy_football_analysis\fantasy_football_data.csv'
df = pd.read_csv(file_path)

# --- Seaborn Visualizations ---

# 1. Violin Plot: Distribution of Points by Position
plt.figure(figsize=(12, 7))
sns.violinplot(data=df, x='Position', y='Points', hue='Position', inner='quartile', palette='viridis', legend=False)
plt.title('Fantasy Points Distribution by Position', fontsize=16)
plt.xlabel('Position', fontsize=12)
plt.ylabel('Points', fontsize=12)
plt.savefig(r'C:\Users\Ryan_\fantasy_football_analysis\points_distribution_by_position.png')
plt.close()

# 2. Correlation Heatmap: Relationships between numerical stats
# Ensure only numerical columns are selected for correlation
numerical_df = df[['Points', 'Touchdowns', 'Yards', 'Week']]
correlation_matrix = numerical_df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Fantasy Stats', fontsize=16)
plt.savefig(r'C:\Users\Ryan_\fantasy_football_analysis\correlation_heatmap.png')
plt.close()

# --- Plotly Interactive Visualizations ---

# 3. 3D Scatter Plot: Points vs. Yards vs. Touchdowns, colored by Position
fig_3d_scatter = px.scatter_3d(df, x='Yards', y='Touchdowns', z='Points', color='Position',
                                 title='3D Scatter Plot of Fantasy Stats by Position',
                                 labels={'Yards': 'Total Yards', 'Touchdowns': 'Total Touchdowns', 'Points': 'Total Points'},
                                 height=600)
fig_3d_scatter.write_html(r'C:\Users\Ryan_\fantasy_football_analysis\interactive_3d_scatter.html')

# 4. Bar Chart: Total Points per Player
total_points_per_player = df.groupby('Player')['Points'].sum().reset_index()
fig_bar_chart = px.bar(total_points_per_player, x='Player', y='Points',
                           title='Total Fantasy Points per Player',
                           labels={'Player': 'Player Name', 'Points': 'Total Points'},
                           color='Points', color_continuous_scale='viridis') # Changed colorscale to 'viridis'
fig_bar_chart.update_layout(xaxis={'categoryorder': 'total descending'})
fig_bar_chart.write_html(r'C:\Users\Ryan_\fantasy_football_analysis\interactive_total_points_bar_chart.html')

# --- Matplotlib Visualization ---

# 5. Line Plot: Points over Week for selected players
# Select a few players for the line plot
selected_players = ["Patrick Mahomes", "Christian McCaffrey", "Tyreek Hill"]
filtered_df = df[df['Player'].isin(selected_players)]

plt.figure(figsize=(12, 7))
sns.lineplot(data=filtered_df, x='Week', y='Points', hue='Player', marker='o')
plt.title('Fantasy Points Over Weeks for Selected Players', fontsize=16)
plt.xlabel('Week', fontsize=12)
plt.ylabel('Points', fontsize=12)
plt.xticks(df['Week'].unique()) # Ensure all weeks are shown as ticks
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig(r'C:\Users\Ryan_\fantasy_football_analysis\points_over_weeks_line_plot.png')
plt.close()

print("Successfully created fantasy football visualizations.")