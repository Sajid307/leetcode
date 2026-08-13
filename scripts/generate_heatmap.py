import json
from datetime import date, datetime, timedelta, timezone

with open(
    "calendar.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)

calendar = data.get("calendar", {})


# ---------------------------------------------------------
# Convert LeetCode timestamps to date -> submission count
# ---------------------------------------------------------

daily_counts = {}

for timestamp, count in calendar.items():

    timestamp = int(timestamp)

    day = datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc
    ).date()

    daily_counts[day] = int(count)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

CELL = 11
GAP = 3

LEFT = 35
TOP = 48

ROWS = 7
COLS = 53

WIDTH = 720
HEIGHT = 150

BACKGROUND = "#0d1117"

LEVELS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353"
]


def get_level(count):
    if count == 0:
        return 0

    if count <= 2:
        return 1

    if count <= 5:
        return 2

    if count <= 10:
        return 3

    return 4


# ---------------------------------------------------------
# Find latest date
# ---------------------------------------------------------

today = date.today()

# Start 365 days ago
start_date = today - timedelta(days=364)

# Move backwards to Sunday.
# This makes the first column a complete calendar week.
start_date -= timedelta(
    days=(start_date.weekday() + 1) % 7
)


# ---------------------------------------------------------
# Generate SVG
# ---------------------------------------------------------

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
width="100%"
height="100%"
rx="12"
fill="{BACKGROUND}"/>

<text
x="20"
y="25"
fill="#ffffff"
font-size="16"
font-family="Arial, sans-serif"
font-weight="bold">
LeetCode Activity — Last 365 Days
</text>
'''


# ---------------------------------------------------------
# Month labels
# ---------------------------------------------------------

previous_month = None

for col in range(COLS):

    column_date = start_date + timedelta(
        days=col * 7
    )

    month = column_date.strftime("%b")

    if month != previous_month:

        x = LEFT + col * (CELL + GAP)

        svg += f'''
<text
x="{x}"
y="39"
fill="#8b949e"
font-size="10"
font-family="Arial, sans-serif">
{month}
</text>
'''

        previous_month = month


# ---------------------------------------------------------
# Weekday labels
# ---------------------------------------------------------

weekday_labels = {
    1: "Mon",
    3: "Wed",
    5: "Fri"
}

for row, label in weekday_labels.items():

    y = (
        TOP
        + row * (CELL + GAP)
        + 9
    )

    svg += f'''
<text
x="5"
y="{y}"
fill="#8b949e"
font-size="9"
font-family="Arial, sans-serif">
{label}
</text>
'''


# ---------------------------------------------------------
# Draw 365-day calendar
# ---------------------------------------------------------

for col in range(COLS):

    for row in range(ROWS):

        current_day = (
            start_date
            + timedelta(days=col * 7 + row)
        )

        # Don't render dates beyond today
        if current_day > today:
            continue

        count = daily_counts.get(
            current_day,
            0
        )

        level = get_level(count)

        x = (
            LEFT
            + col * (CELL + GAP)
        )

        y = (
            TOP
            + row * (CELL + GAP)
        )

        svg += f'''
<rect
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="2"
fill="{LEVELS[level]}">

<title>
{current_day}: {count} submissions
</title>

</rect>
'''


# ---------------------------------------------------------
# Legend
# ---------------------------------------------------------

legend_y = 135
legend_x = 540

svg += '''
<text
x="485"
y="145"
fill="#8b949e"
font-size="10"
font-family="Arial, sans-serif">
Less
</text>
'''

for i, color in enumerate(LEVELS):

    x = (
        legend_x
        + i * 17
    )

    svg += f'''
<rect
x="{x}"
y="{legend_y - 10}"
width="11"
height="11"
rx="2"
fill="{color}"/>
'''


svg += '''
<text
x="630"
y="145"
fill="#8b949e"
font-size="10"
font-family="Arial, sans-serif">
More
</text>

</svg>
'''


# ---------------------------------------------------------
# Write SVG
# ---------------------------------------------------------

with open(
    "profile/heatmap.svg",
    "w",
    encoding="utf-8"
) as file:

    file.write(svg)


print("Generated proper 365-day LeetCode heatmap.")
