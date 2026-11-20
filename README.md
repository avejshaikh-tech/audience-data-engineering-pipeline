# Audience Data Engineering Pipeline

A hands-on ETL project that validates audience event CSV data, loads accepted events into PostgreSQL staging, and builds user/event-type dimensions and an audience-events fact table.

## Tech stack
Python, Pandas, PostgreSQL, psycopg2, python-dotenv, pytest, Python logging.

## Pipeline flow
`data/raw/audience_events.csv` → `src/ingest.py` (validate and deduplicate) → `data/processed/` (valid and rejected CSVs) → `src/load.py` (PostgreSQL staging) → `src/transform.py` (dimensions and fact table). `run_pipeline.py` runs the steps in sequence.

## Data-quality checks
- Required `user_id` is present
- `event_type` is one of `page_view`, `click`, `video_play`
- `event_timestamp` matches `YYYY-MM-DD HH:MM:SS`
- Duplicate `event_id` values are removed from accepted events

Sample dataset: **14 input rows, 10 accepted rows, 4 rejected rows (including 1 duplicate)**.

## Local setup
1. Install Python and PostgreSQL. Create a database (e.g., `company_db`).
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Create tables: `psql -U postgres -d company_db -f sql/schema.sql`
5. Copy `.env.example` to `.env` and set your **local** PostgreSQL credentials. Never commit `.env`.
6. Run: `python run_pipeline.py`
7. Test the processed sample files: `python -m pytest -q`

## Rerun behavior
The staging, dimension and fact inserts use `ON CONFLICT DO NOTHING` with unique/primary keys to avoid inserting the same keys twice. This does **not** update changed records; it is not an UPSERT implementation.

## Notes
- This is a local learning project, not a deployed production system.
- The SQL schema was added for repository reproducibility and should be verified against your local PostgreSQL schema before using an existing database.
- Automated tests currently validate the processed sample CSV files, not the live database or full end-to-end run.
- The provided CSV data is sample event data. Do not upload proprietary customer or employer data.
