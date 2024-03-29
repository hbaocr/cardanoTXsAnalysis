import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import seaborn as sns

dtbName = 'EpocInfo.sqlite'


def read_data_last( days):
    conn = sqlite3.connect(dtbName)
    c = conn.cursor()
    
    # Calculate the start date for the last 12 months
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days)
    
    # Query the data for the last 12 months
    c.execute("SELECT * FROM epochinfo WHERE start >= ?", (start_date,))
    data = c.fetchall()
    print(data)
    # Close the connection
    conn.close()
    
    return data




# Fetch the data
data = read_data_last(365*2)

# Extract the startTime and txCount from the data
start_times = [row[1] for row in data]
txsPdays = [row[8] for row in data]

# Extract the startTime and txCount from the data
start_times = [datetime.datetime.strptime(row[1], "%Y/%m/%d %H:%M:%S") for row in data]
txsPdays = [row[8] for row in data]

# # Plot the data
# fig, ax = plt.subplots()
# ax.plot(start_times, txsPdays)

# # Format the x-axis to show the month/year
# ax.xaxis.set_major_locator(mdates.MonthLocator())
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

# #plt.xlabel('Start Time')

# plt.ylabel('TXs per Day')
# plt.title('Cardano TXs per Day in the last 12 months')
# plt.xticks(rotation=45)

# # Turn on the grid
# plt.grid(True)

# plt.show()





# Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=['epoch', 'start', 'end', 'blocknumber', 'nAccs', 'nTx', 'rewards', 'output', 'txsPday'])

# # Convert the 'start' column to datetime format
# df['start'] = pd.to_datetime(df['start'])

# # Extract the month from the 'start' column
# df['month'] = df['start'].dt.month

# # Create a boxplot of txsPday by month
# sns.boxplot(x='month', y='txsPday', data=df)

# # Set the labels and title
# plt.xlabel('Month')
# plt.ylabel('TXs per Day')
# plt.title('Boxplot of TXs per Day by Month')

# # Rotate the x-axis labels
# plt.xticks(rotation=45)
# plt.grid(True)

# # Show the plot
# plt.show()
# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# First subplot: Line plot of start times and txsPdays
ax1.plot(start_times, txsPdays)
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
ax1.set_ylabel('TXs per Day')
ax1.set_title('Cardano TXs')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
ax1.grid(True)

# Second subplot: Boxplot of txsPday by month/year
df['start'] = pd.to_datetime(df['start'])
df['month_year'] = df['start'].dt.strftime('%m/%Y')
df = df.sort_values('start')
sns.boxplot(x='month_year', y='txsPday', data=df, ax=ax2)
ax2.set_xlabel('Month/Year')
ax2.set_ylabel('TXs per Day')
ax2.set_title('')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
ax2.grid(True)

# Adjust the spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()