import json

with open(
    "activity.json",
    "r",
    encoding="utf-8"
) as file:
    activity = json.load(file)


recent = []

for entry in activity.get("daily", []):

    for problem in entry.get("problems", []):

        recent.append({
            "date": entry["date"],
            "title": problem["title"],
            "slug": problem["slug"],
            "language": problem["language"]
        })


# Newest first
recent.sort(
    key=lambda x: x["date"],
    reverse=True
)

# Show latest 10 problems
recent = recent[:10]


with open(
    "profile/recent-problems.md",
    "w",
    encoding="utf-8"
) as file:

    file.write("# 🧩 Recent LeetCode Problems\n\n")

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
                f"https://leetcode.com/problems/{slug}/"
            )

            file.write(
                f"- **[{title}]({url})** "
                f"— `{language}` · `{date}`\n"
            )


print(
    f"Generated profile/recent-problems.md "
    f"with {len(recent)} problems."
)
