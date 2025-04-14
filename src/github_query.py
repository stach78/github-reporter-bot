import requests

class GitHubQuery:
    def __init__(self, repo_url, token):
        self.repo_url = repo_url
        self.token = token

    def get_commit_lines(self, date_since, author):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # === GET COMMITS MADE TODAY ===
        params = {
            "since": date_since,
            "author": author,
            "per_page": 100,
        }

        response = requests.get(self.repo_url, headers=headers, params=params)
        response.raise_for_status()
        commits = response.json()

        # === FETCH STATS FOR EACH COMMIT ===
        total_lines_added = 0
        detailed_info = []

        for commit in commits:
            commit_url = commit["url"]
            commit_data = requests.get(commit_url, headers=headers).json()
            additions = commit_data.get("stats", {}).get("additions", 0)
            deletions = commit_data.get("stats", {}).get("deletions", 0)
            message = commit_data.get("commit", {}).get("message", "")
            total_lines_added += additions + deletions
            detailed_info.append((additions, deletions, message))

        return total_lines_added, detailed_info

