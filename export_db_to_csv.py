import sqlite3
import pandas as pd

# Database file path
db_path = r'C:\Users\Ryan_\fantasy_football_analysis\espn_fantasy_football.db'

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Connected to database: {db_path}")

# Get list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name_tuple in tables:
    table_name = table_name_tuple[0]
    output_csv_path = f'C:\\Users\\Ryan_\\fantasy_football_analysis\\{table_name}.csv'
    
    try:
        # Read table into a pandas DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        
        # Save DataFrame to CSV
        df.to_csv(output_csv_path, index=False)
        print(f"Successfully exported table '{table_name}' to {output_csv_path}")
    except Exception as e:
        print(f"Error exporting table '{table_name}': {e}")

conn.close()
print("\nDatabase export to CSVs complete.")
