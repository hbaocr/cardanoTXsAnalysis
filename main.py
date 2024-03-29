# import sqlite3

# #ffwf
# def initialize_database():
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()

#     # Create tables and perform other initialization tasks
#     # ...

#     conn.commit()
#     conn.close()

# # Call the function to initialize the database
# initialize_database()



import sqlite3
import requests

dtbName = 'blockInfo.sqlite'


def create_table_if_not_exists():
    conn = sqlite3.connect(dtbName)
    c = conn.cursor()
    # Create the table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS blockinfo
                    (blocknumber INTEGER, epoch INTEGER, createdAt DATETIME, nTx INTEGER, fee REAL, output REAL)''')
    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

def upsert_data(blocknumber, epoch, createdAt, nTx, fee, output):
    conn = sqlite3.connect(dtbName)
    c = conn.cursor()
    
    # Check if the data already exists in the table
    c.execute("SELECT * FROM blockinfo WHERE blocknumber = ?", (blocknumber,))
    existing_data = c.fetchone()
    
    if existing_data:
        # Update the existing data
        # c.execute("UPDATE blockinfo SET epoch = ?, createdAt = ?, nTx = ?, fee = ?, output = ? WHERE blocknumber = ?",
        #             (epoch, createdAt, nTx, fee, output, blocknumber))
        print("Data already exists at blocknumber: ", blocknumber)
        return
    else:
        # Insert the new data
        c.execute("INSERT INTO blockinfo (blocknumber, epoch, createdAt, nTx, fee, output) VALUES (?, ?, ?, ?, ?, ?)",
                    (blocknumber, epoch, createdAt, nTx, fee, output))
    
    # Save (commit) the changes
    conn.commit()
    conn.close()




create_table_if_not_exists()
upsert_data(17, 18, '2021-09-01 00:00:00', 1, 0.1, 0.9)

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
url="https://api.beta.explorer.cardano.org/api/v1/blocks?page={p}&size=100&sort=".format(p=1)
print(url)
data = fetch_data(url)
if data:
    # Process the data
    print(data)