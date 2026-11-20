import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Step 1: Load database configuration
load_dotenv()

# Step 2: Read validated audience events
df = pd.read_csv("data/processed/valid_events.csv")

# Step 3: Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "company_db"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.environ["DB_PASSWORD"]
)

print("Database connection successful")

try:
    with conn:
        with conn.cursor() as cursor:
            # Step 4: Insert each validated event
            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO staging_audience_events
                        (event_id, user_id, event_type, event_timestamp)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (event_id) DO NOTHING
                    """,
                    (
                        row["event_id"],
                        row["user_id"],
                        row["event_type"],
                        row["event_timestamp"]
                    )
                )

    print("Data loading completed successfully")
    print("Records read from CSV:", len(df))

finally:
    conn.close()