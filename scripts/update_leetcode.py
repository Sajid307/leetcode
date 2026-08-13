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


def graphql(query, variables):
    payload = json.dumps({
        "query": query,
        "variables": variables
    }).encode("utf-8")

    request = urllib.request.Request(
        LEETCODE_API,
        data=payload,
        headers=HEADERS
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


# ---------------------------------------------------------
# 1. Fetch profile statistics
# ---------------------------------------------------------

PROFILE_QUERY = """
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
  }
}
"""

profile_data = graphql(
    PROFILE_QUERY,
    {"username": USERNAME}
)

user = profile_data.get("data", {}).get("matchedUser")

if not user:
    raise RuntimeError(
        f"Unable to find LeetCode user: {USERNAME}"
    )


stats = {}

for item in user["submitStats"]["acSubmissionNum"]:
    stats[item["difficulty"]] = {
        "count": item["count"],
        "submissions": item["submissions"]
    }


# ---------------------------------------------------------
# 2. Save statistics
# ---------------------------------------------------------

stats_result = {
    "username": USERNAME,
    "lastUpdated": datetime.now(timezone.utc).isoformat(),
    "ranking": user["profile"]["ranking"],
    "stats": stats
}

with open("stats.json", "w", encoding="utf-8") as file:
    json.dump(
        stats_result,
        file,
        indent=2
    )


# ---------------------------------------------------------
# 3. Fetch recent submissions
# ---------------------------------------------------------

SUBMISSIONS_QUERY = """
query recentAcSubmissions(
    $username: String!,
    $limit: Int!
) {
  recentAcSubmissionList(
    username: $username,
    limit: $limit
  ) {
    id
    title
    titleSlug
    timestamp
    lang
  }
}
"""

submission_data = graphql(
    SUBMISSIONS_QUERY,
    {
        "username": USERNAME,
        "limit": 20
    }
)

submissions = (
    submission_data
    .get("data", {})
    .get("recentAcSubmissionList", [])
)


# ---------------------------------------------------------
# 4. Load existing activity
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# 5. Group submissions by date
# ---------------------------------------------------------

daily_map = {
    entry["date"]: entry
    for entry in activity.get("daily", [])
}

for submission in submissions:

    timestamp = int(submission["timestamp"])

    date = datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc
    ).strftime("%Y-%m-%d")

    problem = {
        "title": submission["title"],
        "slug": submission["titleSlug"],
        "language": submission["lang"]
    }

    if date not in daily_map:

        daily_map[date] = {
            "date": date,
            "problems": []
        }

    existing = daily_map[date]["problems"]

    # Avoid duplicate submissions
    if not any(
        p["slug"] == problem["slug"]
        for p in existing
    ):
        existing.append(problem)


# ---------------------------------------------------------
# 6. Sort activity
# ---------------------------------------------------------

daily = list(daily_map.values())

for entry in daily:
    entry["problems"].sort(
        key=lambda p: p["title"]
    )

daily.sort(
    key=lambda x: x["date"],
    reverse=True
)


# ---------------------------------------------------------
# 7. Save activity
# ---------------------------------------------------------

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


print("LeetCode statistics updated.")
print(f"Recent accepted submissions: {len(submissions)}")
print(f"Tracked days: {len(daily)}")
