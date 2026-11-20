from logger_config import logger
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

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

            # Step 1: Load unique users
            cursor.execute("""
                INSERT INTO dim_user (user_id)
                SELECT DISTINCT user_id
                FROM staging_audience_events
                WHERE user_id IS NOT NULL
                ON CONFLICT (user_id) DO NOTHING;
            """)
            print("New users inserted:", cursor.rowcount)

            # Step 2: Load unique event types
            cursor.execute("""
                INSERT INTO dim_event_type (event_type)
                SELECT DISTINCT event_type
                FROM staging_audience_events
                WHERE event_type IS NOT NULL
                ON CONFLICT (event_type) DO NOTHING;
            """)
            print("New event types inserted:", cursor.rowcount)

            # Step 3: Load audience events into fact table
            cursor.execute("""
                INSERT INTO fact_audience_events (
                    event_id,
                    user_key,
                    event_type_key,
                    event_timestamp
                )
                SELECT
                    s.event_id,
                    u.user_key,
                    e.event_type_key,
                    s.event_timestamp
                FROM staging_audience_events s
                JOIN dim_user u
                    ON s.user_id = u.user_id
                JOIN dim_event_type e
                    ON s.event_type = e.event_type
                ON CONFLICT (event_id) DO NOTHING;
            """)
            print("New fact events inserted:", cursor.rowcount)

    print("Warehouse transformation completed successfully")
    logger.info("Warehouse transformation completed successfully")

except Exception as error:
    print("Transformation failed:", error)
    logger.exception("Warehouse transformation failed")
    raise

finally:
    conn.close()