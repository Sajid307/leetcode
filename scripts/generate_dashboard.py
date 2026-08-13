import json
from datetime import datetime

with open(
    "activity.json",
    "r",
    encoding="utf-8"
) as file:

    activity = json.load(file)


daily = activity.get(
    "daily",
    []
)


recent = []

for entry in daily:

    for problem in entry.get(
        "problems",
        []
    ):

        recent.append({
            "date": entry["date"],
            "title": problem["title"],
            "slug": problem["slug"],
            "language": problem["language"]
        })


recent.sort(
    key=lambda x: x["date"],
    reverse=True
)


recent = recent[:10]


with open(
    "profile/recent-problems.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "## 🧩 Recent LeetCode Problems\n\n"
    )

    if not recent:

        file.write(
            "No recent problems tracked yet.\n"
        )

    else:

        for problem in recent:

            title = problem["title"]
            slug = problem["slug"]
            date = problem["date"]
            language = problem["language"]

            url = (
                "https://leetcode.com/problems/"
                f"{slug}/"
            )

            file.write(
                f"- **[{title}]({url})** — "
                f"`{language}` · `{date}`\n"
            )


print(
    f"Generated recent-problems.md "
    f"with {len(recent)} problems."
)
