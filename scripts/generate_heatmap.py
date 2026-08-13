import json
from datetime import datetime, timezone

with open(
    "calendar.json",
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)


calendar = data.get(
    "calendar",
    {}
)


# ---------------------------------------------------------
# Convert timestamps to daily counts
# ---------------------------------------------------------

days = []

for timestamp, count in calendar.items():

    timestamp = int(timestamp)

    date = datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc
    ).date()

    days.append(
        (date, int(count))
    )


days.sort()


# ---------------------------------------------------------
# Keep approximately one year
# ---------------------------------------------------------

if days:

    latest_date = days[-1][0]

    days = [
        item
        for item in days
        if (
            latest_date - item[0]
        ).days <= 365
    ]


# ---------------------------------------------------------
# Heatmap configuration
# ---------------------------------------------------------

CELL = 12
GAP = 3

ROWS = 7
COLS = 53

WIDTH = 760
HEIGHT = 155


def intensity(count):

    if count == 0:
        return "#161b22"

    if count <= 2:
        return "#0e4429"

    if count <= 5:
        return "#006d32"

    if count <= 10:
        return "#26a641"

    return "#39d353"


counts = {
    day: count
    for day, count in days
}


# ---------------------------------------------------------
# Generate SVG
# ---------------------------------------------------------

svg = f"""
<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
width="100%"
height="100%"
rx="12"
fill="#0d1117"/>

<text
x="20"
y="25"
fill="#ffffff"
font-size="16"
font-family="Arial"
font-weight="bold">
LeetCode Activity — Last 365 Days
</text>
"""


# ---------------------------------------------------------
# Draw cells
# ---------------------------------------------------------

for col in range(COLS):

    for row in range(ROWS):

        index = (
            col * ROWS
            + row
        )

        if index >= len(days):
            continue

        day, count = days[index]

        x = (
            20
            + col * (CELL + GAP)
        )

        y = (
            40
            + row * (CELL + GAP)
        )

        svg += f"""
<rect
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="2"
fill="{intensity(count)}">

<title>
{day}: {count} submissions
</title>

</rect>
"""


# ---------------------------------------------------------
# Legend
# ---------------------------------------------------------

legend_x = 640
legend_y = 135

legend = [
    ("Less", "#161b22"),
    ("", "#0e4429"),
    ("", "#006d32"),
    ("", "#26a641"),
    ("More", "#39d353")
]

for i, (_, color) in enumerate(legend):

    svg += f"""
<rect
x="{legend_x + i * 18}"
y="{legend_y}"
width="12"
height="12"
rx="2"
fill="{color}"/>
"""


svg += f"""
<text
x="20"
y="{HEIGHT - 10}"
fill="#8b949e"
font-size="11"
font-family="Arial">
Daily submissions
</text>

</svg>
"""


with open(
    "profile/heatmap.svg",
    "w",
    encoding="utf-8"
) as file:

    file.write(svg)


print("Generated profile/heatmap.svg")
