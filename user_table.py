import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ.get("DATABASE_URL")

connections = psycopg2.connect(database_url)
cursor = connections.cursor()
cursor.execute("""CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
);
               """)

connections.commit()
cursor.close()
connections.close()