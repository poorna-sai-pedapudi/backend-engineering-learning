import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host = "localhost",
    database = "backend_learning",
    user = "postgres",
    password = "mahimhari69",
    cursor_factory=RealDictCursor

    
)

cursor = conn.cursor()