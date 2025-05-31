from datetime import datetime

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        print("⚠️ Please use HH:MM format (e.g., 14:30).")
        return None
