import pandas as pd

# Step 1: Define the CSV file location
file_path = "data/raw/audience_events.csv"

# Step 2: Read the CSV
df = pd.read_csv(file_path)

# Step 3: Display the first five records
print("First 5 records:")
print(df.head())

# Step 4: Display total number of records
print("\nTotal records:", len(df))

# Step 5: Display missing values
print("\nMissing values:")
print(df.isnull().sum())

# Step 5: Validate required user IDs
valid_user = df["user_id"].notna()

# Step 6: Validate event types
allowed_events = ["page_view", "click", "video_play"]
valid_event = df["event_type"].isin(allowed_events)

# Step 7: Validate timestamps
parsed_timestamps = pd.to_datetime(
    df["event_timestamp"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
)
valid_timestamp = parsed_timestamps.notna()

# Step 8: Separate invalid records
valid_mask = valid_user & valid_event & valid_timestamp

valid_df = df[valid_mask].copy()
invalid_df = df[~valid_mask].copy()

# Step 9: Identify and remove duplicate events
duplicate_mask = valid_df.duplicated(
    subset=["event_id"],
    keep="first"
)

duplicates_df = valid_df[duplicate_mask].copy()
valid_df = valid_df[~duplicate_mask].copy()

# Step 10: Combine rejected records
rejected_df = pd.concat(
    [invalid_df, duplicates_df],
    ignore_index=True
)

# Step 11: Save processed datasets
valid_df.to_csv("data/processed/valid_events.csv", index=False)
rejected_df.to_csv("data/processed/rejected_events.csv", index=False)

# Step 12: Display validation summary
print("\nDATA QUALITY SUMMARY")
print("Total input records:", len(df))
print("Valid records:", len(valid_df))
print("Rejected records:", len(rejected_df))
print("Duplicate records:", len(duplicates_df))