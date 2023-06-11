import psycopg2
import os
from dotenv import load_dotenv

### Setting up the postgresql database
# sudo -i -u postgres
# createuser --interactive
# name = admin
# superuser = y
# createdb wscsquash

load_dotenv()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
