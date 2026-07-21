from database import SessionLocal
from models import Activity

session = SessionLocal()
activities = session.query(Activity).order_by(Activity.start_date.desc()).limit(5).all()

for a in activities:
    print(f"{a.start_date.date()} | {a.name} | {a.distance_meters/1000:.2f}km | {a.duration_seconds/60:.1f}min | HR: {a.average_heartrate}")

session.close()