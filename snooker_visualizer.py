import pandas as pd
import matplotlib.pyplot as plt
import gspread
import os
import datetime

# --- Authenticate and Load Data ---
with open('service_account.json', 'w') as f:
    f.write(os.environ['GDRIVE_API_KEY'])

gc = gspread.service_account(filename='service_account.json')

# Replace with your actual spreadsheet key (from the URL)
sh = gc.open_by_key('1B1UQMi9p5WOd-TOFVkoRXDLuee-8z94gb4_KQz9gT9s')
worksheet = sh.get_worksheet(0)
data = worksheet.get_all_values()

# Convert to a pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])
print("Data loaded successfully from Google Sheets!")

# --- Data Cleaning and Pre-processing ---
# Standardize column names for easier use
df.rename(columns={'Date of Frame': 'Date'}, inplace=True)
player_scores = ['Score - Pete', 'Score - Torqs', 'Score - Alex']
winner_column = 'Winner'

# Convert relevant columns to appropriate data types
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
for col in player_scores:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# --- Data Analysis & Visualization ---

# Get total wins per player
winner_counts = df[winner_column].value_counts()

# Calculate total points and average points
total_points_dict = defaultdict(int)
for _, row in df.iterrows():
    for player_col in player_scores:
        player_name = player_col.replace('Score - ', '')
        score = row[player_col]
        if pd.notna(score):
            total_points_dict[player_name] += score

total_points_series = pd.Series(total_points_dict).sort_values(ascending=False)

# Calculate average points per game
games_played = df.groupby(winner_column).size()
avg_points_series = total_points_series / games_played
avg_points_series = avg_points_series.sort_values(ascending=False)

# Get daily winner percentage
daily_winner_counts = df.groupby('Date')[winner_column].value_counts()
daily_winner_series = daily_winner_counts.loc[daily_winner_counts.groupby(level=0).idxmax()].sort_values()
daily_winner_percentage = daily_winner_series.index.get_level_values(1).value_counts(normalize=True) * 100
daily_winner_percentage.sort_values(ascending=False, inplace=True)


# --- Plotting Functions ---

def create_and_save_plot(data, title, xlabel, ylabel, filename, color):
    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', color=color)
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Graph '{filename}' saved!")


# --- Generate Graphs ---
create_and_save_plot(winner_counts, 'Total Wins Per Player', 'Player', 'Number of Wins', 'game_wins.png', '#1f77b4')
create_and_save_plot(avg_points_series, 'Average Points Per Game', 'Player', 'Average Points', 'avg_points.png', '#ff7f0e')
create_and_save_plot(total_points_series, 'Total Points Scored', 'Player', 'Total Points', 'total_points.png', '#2ca02c')
create_and_save_plot(daily_winner_percentage, 'Daily Win Percentage', 'Player', 'Percentage of Days Won', 'daily_winner_percentage.png', '#9467bd')

print("All graphs generated and saved.")