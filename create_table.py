import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ.get("DATABASE_URL")

connections = psycopg2.connect(database_url)
cursor = connections.cursor()
cursor.execute("""
               CREATE TABLE expense (
                   id SERIAL PRIMARY KEY,
                   habit TEXT NOT NULL,
                   frequency TEXT NOT NULL,
                   streak NUMERIC NOT NULL
                   
               );
               """)
connections.commit()
cursor.close()
connections.close()