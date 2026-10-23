
import os
import psycopg2
from dotenv import load_dotenv

# Load the .env file from the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )


if __name__=="__main__":
    try:
        connection=get_connection()
        print("connection succesfully")
        connection.close()
    except Exception as e:
        print("connection failed")
        print(e)


