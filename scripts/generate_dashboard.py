import json
import re

PROFILE_README = "../Sajid307/README.md"

with open(
    "activity.json",
    "r",
    encoding="utf-8"
) as file:

    activity = json.load(file)


recent = []

for entry in activity.get("daily", []):

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


recent = recent[:8]


lines = [
    "### 🧠 Recent Problems",
    "",
    "<!-- LEETCODE:START -->",
    ""
]


if recent:

    for problem in recent:

        title = problem["title"]
        slug = problem["slug"]
        language = problem["language"]
        date = problem["date"]

        url = (
            "https://leetcode.com/problems/"
            f"{slug}/"
        )

        lines.append(
            f"- [{title}]({url}) "
            f"— `{language}` · `{date}`"
        )

else:

    lines.append(
        "No recent problems tracked yet."
    )


lines.extend([
    "",
    "<!-- LEETCODE:END -->"
])


new_section = "\n".join(lines)


with open(
    PROFILE_README,
    "r",
    encoding="utf-8"
) as file:

    readme = file.read()


pattern = (
    r"### 🧠 Recent Problems"
    r".*?"
    r"<!-- LEETCODE:END -->"
)


updated = re.sub(
    pattern,
    new_section,
    readme,
    flags=re.DOTALL
)


with open(
    PROFILE_README,
    "w",
    encoding="utf-8"
) as file:

    file.write(updated)


print("Updated profile README.")
