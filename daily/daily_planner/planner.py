from datetime import timedelta
from .utils import parse_time

def run_planner():
    print("🌸 Welcome to the Daily Schedule Planner!")
    print("Enter your tasks for today. Type 'done' when you're finished.\n")

    tasks = []
    total_minutes = 0

    while True:
        task_name = input("📝 Task name (or 'done' to finish): ").strip()
        if task_name.lower() == 'done':
            break

        time_mode = input("⏳ Enter time as (1) Start & End Time or (2) Duration? [1/2]: ").strip()

        duration = None

        if time_mode == '1':
            while True:
                start_time = parse_time(input("Start time (HH:MM): "))
                end_time = parse_time(input("End time (HH:MM): "))
                if start_time and end_time:
                    diff = end_time - start_time
                    if diff.total_seconds() < 0:
                        diff += timedelta(days=1)  # handle midnight crossing
                    duration = diff.total_seconds() / 60
                    break
        elif time_mode == '2':
            while True:
                try:
                    hours = float(input("Hours spent: "))
                    minutes = float(input("Minutes spent: "))
                    duration = hours * 60 + minutes
                    break
                except ValueError:
                    print("⚠️ Please enter numbers.")
        else:
            print("⚠️ Invalid option. Skipping task.")
            continue

        tasks.append((task_name, duration))
        total_minutes += duration

        print(f"✅ Added: {task_name} ({duration/60:.2f} hours)\n")

    # Summary
    print("\n📊 Daily Summary:")
    for name, minutes in tasks:
        print(f" - {name}: {minutes/60:.2f} hours")
    print(f"🕒 Total time spent: {total_minutes/60:.2f} hours")
