import json
from datetime import date, timedelta

with open("activity.json", "r", encoding="utf-8") as file:
    activity = json.load(file)

days = {
    entry["date"]
    for entry in activity.get("daily", [])
    if entry.get("problems")
}

if not days:
    current_streak = 0
    max_streak = 0
else:
    dates = sorted(
        (date.fromisoformat(d) for d in days),
        reverse=True
    )

    # Current streak
    current_streak = 0
    current = date.today()

    while current in dates:
        current_streak += 1
        current -= timedelta(days=1)

    # Maximum streak
    sorted_dates = sorted(dates)

    max_streak = 1
    streak = 1

    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] == sorted_dates[i - 1] + timedelta(days=1):
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1


total_problems = sum(
    len(entry.get("problems", []))
    for entry in activity.get("daily", [])
)

result = {
    "username": activity["username"],
    "lastUpdated": activity["lastUpdated"],
    "totalActiveDays": len(days),
    "totalTrackedProblems": total_problems,
    "currentStreak": current_streak,
    "maxStreak": max_streak
}

with open("streak.json", "w", encoding="utf-8") as file:
    json.dump(result, file, indent=2)

print(json.dumps(result, indent=2))
