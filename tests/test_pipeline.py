from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

def test_valid_events_count():
    file_path = BASE_DIR / "data" / "processed" / "valid_events.csv"
    df = pd.read_csv(file_path)

    assert len(df) == 10


def test_no_missing_user_ids():
    file_path = BASE_DIR / "data" / "processed" / "valid_events.csv"
    df = pd.read_csv(file_path)

    assert df["user_id"].notna().all()


def test_no_duplicate_event_ids():
    file_path = BASE_DIR / "data" / "processed" / "valid_events.csv"
    df = pd.read_csv(file_path)

    assert not df["event_id"].duplicated().any()


def test_allowed_event_types():
    file_path = BASE_DIR / "data" / "processed" / "valid_events.csv"
    df = pd.read_csv(file_path)

    allowed = {"page_view", "click", "video_play"}

    assert df["event_type"].isin(allowed).all()


def test_valid_timestamps():
    file_path = BASE_DIR / "data" / "processed" / "valid_events.csv"
    df = pd.read_csv(file_path)

    timestamps = pd.to_datetime(
        df["event_timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce"
    )

    assert timestamps.notna().all()