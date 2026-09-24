import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
database_url = os.environ.get("DATABASe_URL")

connections = psycopg2.connect(database_url)
cursor = connections.cursor()
cursor.execute("""ALTER TABLE habittracker
                ADD COLUMN userid  INTEGER REFERENCES users(id) ;
               """)

connections.commit()
cursor.close()
connections.close()