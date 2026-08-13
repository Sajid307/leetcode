import json
import urllib.request
from datetime import datetime, timezone

USERNAME = "Sajid-307"
LEETCODE_API = "https://leetcode.com/graphql"

QUERY = """
query userProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      realName
      userAvatar
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

payload = json.dumps({
    "query": QUERY,
    "variables": {
        "username": USERNAME
    }
}).encode("utf-8")

request = urllib.request.Request(
    LEETCODE_API,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.loads(response.read().decode("utf-8"))

user = data.get("data", {}).get("matchedUser")

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

result = {
    "username": USERNAME,
    "lastUpdated": datetime.now(timezone.utc).isoformat(),
    "ranking": user["profile"]["ranking"],
    "stats": stats
}

with open("stats.json", "w", encoding="utf-8") as file:
    json.dump(result, file, indent=2)

print(json.dumps(result, indent=2))
