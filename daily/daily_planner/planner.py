from datetime import timedelta
from .utils import parse_time

def process_tasks(task_data):
    tasks = []
    total_minutes = 0

    for item in task_data:
        task_name = item.get("task_name", "Unknown Task")
        time_mode = item.get("time_mode")
        duration = 0

        if time_mode == '1':
            # Handle start & end time
            start_time = parse_time(item.get("start"))
            end_time = parse_time(item.get("end"))
            if start_time and end_time:
                diff = end_time - start_time
                if diff.total_seconds() < 0:
                    diff += timedelta(days=1)
                duration = diff.total_seconds() / 60
        elif time_mode == '2':
            # Handle direct duration
            hours = float(item.get("hours", 0))
            minutes = float(item.get("minutes", 0))
            duration = hours * 60 + minutes

        tasks.append({"task_name": task_name, "duration_hours": round(duration / 60, 2)})
        total_minutes += duration

    summary = {
        "tasks": tasks,
        "total_hours": round(total_minutes / 60, 2)
    }

    return summary
