import csv
from datetime import datetime
from database import SessionLocal, init_db
from models import Activity

def load_activities(csv_path: str) -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def parse_date(date_str: str) -> datetime:
    # Strava format: "Jul 19, 2026, 12:45:20 PM"
    return datetime.strptime(date_str, "%b %d, %Y, %I:%M:%S %p")


def safe_float(value: str) -> float | None:
    """Strava leaves many fields blank; convert '' to None instead of crashing."""
    if value is None or value.strip() == "":
        return None
    return float(value)


def import_activities(csv_path: str):
    init_db()  # make sure tables exist
    session = SessionLocal()

    rows = load_activities(csv_path)
    imported = 0
    skipped = 0

    for row in rows:
        activity_id = row["Activity ID"]

        # Skip if we've already imported this one (avoid duplicates on re-run)
        existing = session.query(Activity).filter_by(strava_id=activity_id).first()
        if existing:
            skipped += 1
            continue

        activity = Activity(
            strava_id=activity_id,
            activity_type=row["Activity Type"],
            name=row["Activity Name"],
            distance_meters=safe_float(row["Distance"]),
            duration_seconds=safe_float(row["Elapsed Time"]),
            elevation_gain_meters=safe_float(row["Elevation Gain"]),
            average_heartrate=safe_float(row["Average Heart Rate"]),
            start_date=parse_date(row["Activity Date"]),
        )
        session.add(activity)
        imported += 1

    session.commit()
    session.close()
    print(f"Imported {imported} new activities, skipped {skipped} duplicates")


if __name__ == "__main__":
    import_activities("data_export.csv")