import json
import os

with open("stats.json", "r", encoding="utf-8") as f:
    stats = json.load(f)

with open("streak.json", "r", encoding="utf-8") as f:
    streak = json.load(f)

total_solved = 0

for difficulty in ["Easy", "Medium", "Hard"]:
    total_solved += stats.get("stats", {}).get(
        difficulty, {}
    ).get("count", 0)


# Support common possible key names
current_streak = (
    streak.get("currentStreak")
    or streak.get("current_streak")
    or 0
)

max_streak = (
    streak.get("maxStreak")
    or streak.get("max_streak")
    or 0
)

active_days = (
    streak.get("activeDays")
    or streak.get("active_days")
    or 0
)


svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="700"
height="110"
viewBox="0 0 700 110">

<rect
width="700"
height="110"
rx="12"
fill="#0d1117"/>

<text
x="25"
y="28"
fill="#ffffff"
font-size="16"
font-family="Arial, sans-serif"
font-weight="bold">
🧩 LeetCode Progress
</text>

<text x="25" y="62"
fill="#8b949e"
font-size="12"
font-family="Arial, sans-serif">
Problems Solved
</text>

<text x="25" y="88"
fill="#ffffff"
font-size="20"
font-family="Arial, sans-serif"
font-weight="bold">
{total_solved}
</text>


<text x="190" y="62"
fill="#8b949e"
font-size="12"
font-family="Arial, sans-serif">
Active Days
</text>

<text x="190" y="88"
fill="#ffffff"
font-size="20"
font-family="Arial, sans-serif"
font-weight="bold">
{active_days}
</text>


<text x="350" y="62"
fill="#8b949e"
font-size="12"
font-family="Arial, sans-serif">
Current Streak
</text>

<text x="350" y="88"
fill="#ffffff"
font-size="20"
font-family="Arial, sans-serif"
font-weight="bold">
🔥 {current_streak}
</text>


<text x="520" y="62"
fill="#8b949e"
font-size="12"
font-family="Arial, sans-serif">
Max Streak
</text>

<text x="520" y="88"
fill="#ffffff"
font-size="20"
font-family="Arial, sans-serif"
font-weight="bold">
🏆 {max_streak}
</text>

</svg>
'''


os.makedirs(
    "profile",
    exist_ok=True
)

with open(
    "profile/metrics.svg",
    "w",
    encoding="utf-8"
) as f:
    f.write(svg)

print("Generated profile/metrics.svg")
