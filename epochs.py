



import sqlite3
import requests
import datetime


dtbName = 'EpocInfo.sqlite'


def create_table_if_not_exists():
    conn = sqlite3.connect(dtbName)
    c = conn.cursor()
    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS epochinfo
                    (epoch INTEGER,start DATETIME,end DATETIME, blocknumber INTEGER,nAccs INTEGER, nTx INTEGER, rewards INTEGER, output INTEGER,txsPday INTEGER)''')
    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()



def upsert_data(epoch, start, end,blocknumber, nAccs, nTx, rewards, output,txsPday):
    conn = sqlite3.connect(dtbName)
    c = conn.cursor()
    # Check if the epoch already exists in the table
    c.execute("SELECT * FROM epochinfo WHERE epoch=?", (epoch,))
    existing_data = c.fetchone()
    if existing_data:
        # Update the existing data
        #c.execute("UPDATE epochinfo SET blocknumber=?, start=?, end=?, nAccs=?, nTx=?, rewards=?, output=? WHERE epoch=?", (blocknumber, start, end, nAccs, nTx, rewards, output, epoch))
        print("Data already exists at epoch: ", epoch)
        return
    else:
        # Insert new data
        c.execute("INSERT INTO epochinfo (epoch, blocknumber, start, end, nAccs, nTx, rewards, output,txsPday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (epoch, blocknumber, start, end, nAccs, nTx, rewards, output,txsPday))
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()


create_table_if_not_exists()

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data from the URL:", url)
        return None

# Example usage
#url="https://api.beta.explorer.cardano.org/api/v1/blocks?page=1&size=100&sort="
#url="https://api.beta.explorer.cardano.org/api/v1/blocks?page={p}&size=100&sort=".format(p=1)
# url="https://api.beta.explorer.cardano.org/api/v1/epochs?page={p}&size=100".format(p=1)
# print(url)
# data = fetch_data(url)
# if data:
#     # Process the data
#     print(data)
def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y/%m/%d %H:%M:%S")
    d2 = datetime.datetime.strptime(d2, "%Y/%m/%d %H:%M:%S")
    return abs((d2 - d1).days)

# Example usage
# startTime = "2024/03/05 21:44:51"
# endTime = "2024/03/10 21:44:51"
# print(days_between(startTime, endTime))



for page in range(0,9):
    url="https://api.beta.explorer.cardano.org/api/v1/epochs?page={p}&size=100".format(p=page)
    data = fetch_data(url)
    if data:
        for epoch in data['data']:
            print(epoch['no'], epoch['startTime'], epoch['endTime'], epoch['blkCount'], epoch['account'], epoch['txCount'], epoch['rewardsDistributed'], epoch['outSum'])
            avg_txs_per_day = int(epoch['txCount'] / days_between(epoch['startTime'], epoch['endTime']))
            upsert_data(epoch['no'], epoch['startTime'], epoch['endTime'], epoch['blkCount'], epoch['account'], epoch['txCount'], epoch['rewardsDistributed'], epoch['outSum'],avg_txs_per_day)
            



def read_data_last_12_months():
    conn = sqlite3.connect(dtbName)
    c = conn.cursor()
    
    # Calculate the start date for the last 12 months
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=180)
    
    # Query the data for the last 12 months
    c.execute("SELECT * FROM epochinfo WHERE start >= ?", (start_date,))
    data = c.fetchall()
    print(data)
    # Close the connection
    conn.close()
    
    return data




   