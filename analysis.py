from datetime import datetime, timedelta
from collections import defaultdict
from database import SessionLocal
from models import Activity

def get_weekly_mileage(session) -> list[dict]:
    """Group all activities into calendar weeks, summing distance per week."""
    activities = session.query(Activity).order_by(Activity.start_date).all()

    weekly = defaultdict(float)
    for a in activities:
        # ISO week: (year, week_number) — groups Mon-Sun consistently
        year, week, _ = a.start_date.isocalendar()
        key = (year, week)
        weekly[key] += a.distance_meters / 1000  # convert to km

    # Sort chronologically
    sorted_weeks = sorted(weekly.items())
    return [{"year": y, "week": w, "km": round(km, 1)} for (y, w), km in sorted_weeks]

def flag_training_risk(weeks: list[dict]) -> list[dict]:
    """Compare each week to the previous one and flag risky jumps or drops."""
    results = []
    for i, week in enumerate(weeks):
        if i == 0:
            results.append({**week, "pct_change": None, "risk_flag": "insufficient_history"})
            continue

        prev_km = weeks[i - 1]["km"]
        curr_km = week["km"]

        if prev_km == 0:
            pct_change = None
            flag = "insufficient_history"
        else:
            pct_change = round((curr_km - prev_km) / prev_km * 100, 1)
            if pct_change > 30:
                flag = "overtraining_risk"
            elif pct_change < -40:
                flag = "significant_drop"  # could be planned taper OR missed training — needs context
            else:
                flag = "on_track"

        results.append({**week, "pct_change": pct_change, "risk_flag": flag})
    return results


if __name__ == "__main__":
    session = SessionLocal()
    weeks = get_weekly_mileage(session)
    session.close()

    flagged = flag_training_risk(weeks[-8:])
    for w in flagged:
        pct = f"{w['pct_change']:+.1f}%" if w['pct_change'] is not None else "—"
        print(f"{w['year']}-W{w['week']:02d}: {w['km']}km  ({pct})  [{w['risk_flag']}]")
