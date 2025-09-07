import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the data from your CSV file
try:
    df = pd.read_csv('snooker_data.csv')
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Error: snooker_data.csv not found. Make sure the file is in the same folder.")
    exit()

# Step 2: Analyze the 'Winner' column and count wins
winner_counts = df['Winner'].value_counts()

# Step 3: Create a bar chart for the wins
plt.style.use('seaborn-v0_8-whitegrid')
winner_counts.plot(kind='bar', color='#1f77b4')
plt.title('Total Wins Per Player', fontsize=16)
plt.xlabel('Player', fontsize=12)
plt.ylabel('Number of Wins', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout() # Adjusts plot to prevent labels from being cut off

# Step 4: Save the chart as an image file
plt.savefig('game_wins.png')
print("Graph saved as game_wins.png!")

# Step 5: Display the chart
plt.show()