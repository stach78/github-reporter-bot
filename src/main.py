import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from github_query import GitHubQuery
from mastodon_publisher import MastodonPublisher

def main():
    load_dotenv()

    github_token = os.getenv("GITHUB_TOKEN")
    github_user = os.getenv("GITHUB_USER")
    github_repo = os.getenv("GITHUB_REPO")
    mastodon_token = os.getenv("MASTODON_TOKEN")
    repo_url = f"https://api.github.com/repos/{github_user}/{github_repo}/commits"
    mastodon_base_url = os.getenv("MASTODON_BASE_URL")

    github = GitHubQuery(repo_url, github_token)
    mastodon_publisher = MastodonPublisher(mastodon_base_url, mastodon_token)

    date_since = (datetime.now() - timedelta(days=1)).isoformat()

    lines_committed, detailed_info = github.get_commit_lines(date_since, github_user)

    if lines_committed > 0:
        message = f"Today, the creator committed {lines_committed} lines of code to the project!"
    else:
        message = f"The creator didn't commit any lines of code today, lazy bum."

    mastodon_publisher.post_update(message)
    print(f"Message posted to Mastodon {message}.")

if __name__ == "__main__":
    main()
