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
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_DATABASE"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT")
)
