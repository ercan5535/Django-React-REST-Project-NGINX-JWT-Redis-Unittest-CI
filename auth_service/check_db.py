import psycopg2
import time
import os

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

result=False
for i in range(0, 20): 
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        # Close the connection
        conn.close()
        # Connection successful
        result = True
        break
    except:
        print(f"Tried to connect database for {i} times")
        # Wait 5 seconds until next try
        time.sleep(5)
if not result:
    raise Exception("DB connection failed")

print("DB connection is succesfull")


