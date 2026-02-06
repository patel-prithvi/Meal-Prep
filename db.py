import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="Meal_prep",
        user="postgres",
        password="Prithvi@20",
        host="localhost",
        port=5433
    )
