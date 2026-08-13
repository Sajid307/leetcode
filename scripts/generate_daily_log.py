import json
import os
from datetime import datetime, timezone

TODAY = datetime.now(
    timezone.utc
).strftime("%Y-%m-%d")


with open(
    "activity.json",
    "r",
    encoding="utf-8"
) as file:

    activity = json.load(file)


today_entry = None

for entry in activity.get(
    "daily",
    []
):

    if entry["date"] == TODAY:
        today_entry = entry
        break


os.makedirs(
    "logs",
    exist_ok=True
)


log_file = f"logs/{TODAY}.md"


with open(
    log_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        f"# 🧩 LeetCode — {TODAY}\n\n"
    )

    if not today_entry:

        file.write(
            "No accepted LeetCode problems "
            "recorded today.\n"
        )

    else:

        problems = today_entry.get(
            "problems",
            []
        )

        if not problems:

            file.write(
                "No accepted problems recorded today.\n"
            )

        else:

            file.write(
                f"Problems solved: **{len(problems)}**\n\n"
            )

            for problem in problems:

                title = problem["title"]
                slug = problem["slug"]
                language = problem["language"]

                url = (
                    "https://leetcode.com/problems/"
                    f"{slug}/"
                )

                file.write(
                    f"- [{title}]({url}) "
                    f"— `{language}`\n"
                )


print(
    f"Generated {log_file}"
)
