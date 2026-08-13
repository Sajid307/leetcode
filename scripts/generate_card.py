import json
from html import escape

with open("stats.json", "r", encoding="utf-8") as f:
    stats_data = json.load(f)

with open("streak.json", "r", encoding="utf-8") as f:
    streak_data = json.load(f)

stats = stats_data.get("stats", {})

easy = stats.get("Easy", {}).get("count", 0)
medium = stats.get("Medium", {}).get("count", 0)
hard = stats.get("Hard", {}).get("count", 0)

total = stats.get("All", {}).get("count", easy + medium + hard)

current_streak = streak_data.get("currentStreak", 0)
max_streak = streak_data.get("maxStreak", 0)
active_days = streak_data.get("totalActiveDays", 0)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="700"
height="330"
viewBox="0 0 700 330">

<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#161b22"/>
        <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
</defs>

<rect
    x="5"
    y="5"
    width="690"
    height="320"
    rx="18"
    fill="url(#bg)"
    stroke="#30363d"
    stroke-width="2"
/>

<text
    x="35"
    y="55"
    fill="#ffffff"
    font-size="28"
    font-family="Arial, sans-serif"
    font-weight="bold">
    LeetCode Progress
</text>

<text
    x="35"
    y="82"
    fill="#8b949e"
    font-size="15"
    font-family="Arial, sans-serif">
    @{escape(stats_data["username"])}
</text>

<!-- Total -->

<text
    x="60"
    y="135"
    fill="#58a6ff"
    font-size="34"
    font-family="Arial, sans-serif"
    font-weight="bold">
    {total}
</text>

<text
    x="60"
    y="160"
    fill="#8b949e"
    font-size="14"
    font-family="Arial, sans-serif">
    Problems Solved
</text>

<!-- Easy -->

<text
    x="240"
    y="135"
    fill="#00b8a3"
    font-size="28"
    font-family="Arial, sans-serif"
    font-weight="bold">
    {easy}
</text>

<text
    x="240"
    y="160"
    fill="#8b949e"
    font-size="14"
    font-family="Arial, sans-serif">
    Easy
</text>

<!-- Medium -->

<text
    x="360"
    y="135"
    fill="#ffa116"
    font-size="28"
    font-family="Arial, sans-serif"
    font-weight="bold">
    {medium}
</text>

<text
    x="360"
    y="160"
    fill="#8b949e"
    font-size="14"
    font-family="Arial, sans-serif">
    Medium
</text>

<!-- Hard -->

<text
    x="500"
    y="135"
    fill="#ef4743"
    font-size="28"
    font-family="Arial, sans-serif"
    font-weight="bold">
    {hard}
</text>

<text
    x="500"
    y="160"
    fill="#8b949e"
    font-size="14"
    font-family="Arial, sans-serif">
    Hard
</text>

<!-- Divider -->

<line
    x1="35"
    y1="190"
    x2="665"
    y2="190"
    stroke="#30363d"
/>

<!-- Streak -->

<text
    x="60"
    y="235"
    fill="#f78166"
    font-size="25"
    font-family="Arial, sans-serif"
    font-weight="bold">
    🔥 {current_streak}
</text>

<text
    x="60"
    y="258"
    fill="#8b949e"
    font-size="13"
    font-family="Arial, sans-serif">
    Current Streak
</text>

<!-- Max streak -->

<text
    x="270"
    y="235"
    fill="#f2cc60"
    font-size="25"
    font-family="Arial, sans-serif"
    font-weight="bold">
    🏆 {max_streak}
</text>

<text
    x="270"
    y="258"
    fill="#8b949e"
    font-size="13"
    font-family="Arial, sans-serif">
    Max Streak
</text>

<!-- Active days -->

<text
    x="480"
    y="235"
    fill="#79c0ff"
    font-size="25"
    font-family="Arial, sans-serif"
    font-weight="bold">
    {active_days}
</text>

<text
    x="480"
    y="258"
    fill="#8b949e"
    font-size="13"
    font-family="Arial, sans-serif">
    Active Days
</text>

<text
    x="35"
    y="300"
    fill="#6e7681"
    font-size="12"
    font-family="Arial, sans-serif">
    Automatically updated by GitHub Actions
</text>

</svg>
"""

with open(
    "profile/leetcode.svg",
    "w",
    encoding="utf-8"
) as f:
    f.write(svg)

print("Generated profile/leetcode.svg")
