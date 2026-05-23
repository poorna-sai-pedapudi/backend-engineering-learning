import os
import psycopg2

from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()


# conn = psycopg2.connect(
#     #host = "host.docker.internal",
#     #host="localhost",
#     database = "backend_learning",
#     user = "postgres",
#     password = "mahimhari69",
#     cursor_factory=RealDictCursor
# )

# cursor = conn.cursor()


conn = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    database = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    cursor_factory = RealDictCursor

)

cursor = conn.cursor()