import json
import os
import urllib.request
from datetime import datetime, timezone

USERNAME = "Sajid-307"
LEETCODE_API = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}


def graphql(query, variables=None):
    payload = json.dumps({
        "query": query,
        "variables": variables or {}
    }).encode("utf-8")

    request = urllib.request.Request(
        LEETCODE_API,
        data=payload,
        headers=HEADERS
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    if result.get("errors"):
        raise RuntimeError(
            json.dumps(result["errors"], indent=2)
        )

    return result


QUERY = """
query userProfile($username: String!) {

  matchedUser(username: $username) {

    username

    profile {
      realName
      ranking
    }

    submitStats {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }

    submissionCalendar
  }

  recentAcSubmissionList(
    username: $username
    limit: 20
  ) {
    id
    title
    titleSlug
    timestamp
    lang
  }
}
"""


data = graphql(
    QUERY,
    {
        "username": USERNAME
    }
)

user = (
    data
    .get("data", {})
    .get("matchedUser")
)

if not user:
    raise RuntimeError(
        f"Unable to find LeetCode user: {USERNAME}"
    )


# =========================================================
# Statistics
# =========================================================

stats = {}

for item in user["submitStats"]["acSubmissionNum"]:

    stats[item["difficulty"]] = {
        "count": item["count"],
        "submissions": item["submissions"]
    }


stats_result = {
    "username": USERNAME,
    "lastUpdated": datetime.now(
        timezone.utc
    ).isoformat(),
    "ranking": user["profile"]["ranking"],
    "stats": stats
}


with open(
    "stats.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        stats_result,
        file,
        indent=2
    )


# =========================================================
# Submission Calendar
# =========================================================

calendar_raw = user.get(
    "submissionCalendar"
)

if calendar_raw:
    calendar = json.loads(calendar_raw)
else:
    calendar = {}


calendar_result = {
    "username": USERNAME,
    "lastUpdated": datetime.now(
        timezone.utc
    ).isoformat(),
    "calendar": calendar
}


with open(
    "calendar.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        calendar_result,
        file,
        indent=2
    )


# =========================================================
# Recent Accepted Problems
# =========================================================

submissions = (
    data
    .get("data", {})
    .get("recentAcSubmissionList", [])
)


activity_file = "activity.json"

if os.path.exists(activity_file):

    with open(
        activity_file,
        "r",
        encoding="utf-8"
    ) as file:

        activity = json.load(file)

else:

    activity = {
        "username": USERNAME,
        "lastUpdated": "",
        "daily": []
    }


daily_map = {
    entry["date"]: entry
    for entry in activity.get("daily", [])
}


for submission in submissions:

    timestamp = int(
        submission["timestamp"]
    )

    submitted_date = datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc
    ).strftime("%Y-%m-%d")

    problem = {
        "title": submission["title"],
        "slug": submission["titleSlug"],
        "language": submission["lang"]
    }

    if submitted_date not in daily_map:

        daily_map[submitted_date] = {
            "date": submitted_date,
            "problems": []
        }

    problems = daily_map[
        submitted_date
    ]["problems"]

    if not any(
        p["slug"] == problem["slug"]
        for p in problems
    ):
        problems.append(problem)


daily = list(
    daily_map.values()
)


for entry in daily:

    entry["problems"].sort(
        key=lambda x: x["title"]
    )


daily.sort(
    key=lambda x: x["date"],
    reverse=True
)


activity_result = {
    "username": USERNAME,
    "lastUpdated": datetime.now(
        timezone.utc
    ).isoformat(),
    "daily": daily
}


with open(
    activity_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        activity_result,
        file,
        indent=2
    )


print("===================================")
print("LeetCode update completed")
print("===================================")
print(f"Username: {USERNAME}")
print(f"Recent accepted: {len(submissions)}")
print(f"Calendar days: {len(calendar)}")
print(f"Tracked activity days: {len(daily)}")
