import requests
import csv
import time
from collections import defaultdict

GITHUB_TOKEN = "GITHUB token"
GITHUB_API_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# Define the CSV files for storing data
USERS_CSV = "users.csv"
REPOS_CSV = "repositories.csv"

# Utility function to handle rate limiting
def check_rate_limit():
    response = requests.get(f"{GITHUB_API_URL}/rate_limit", headers=HEADERS)
    rate_data = response.json()
    remaining = rate_data['rate']['remaining']
    reset_time = rate_data['rate']['reset']
    
    if remaining < 10:
        reset_seconds = reset_time - time.time()
        print(f"Rate limit nearly exceeded. Sleeping until reset in {reset_seconds} seconds.")
        time.sleep(max(reset_seconds, 0))

# Clean company name format
def clean_company_name(company):
    return (company.strip().lstrip('@').upper() if company else "")

# Fetch user details
def fetch_user_details(user_login):
    check_rate_limit()
    response = requests.get(f"{GITHUB_API_URL}/users/{user_login}", headers=HEADERS)
    return response.json() if response.status_code == 200 else None

# Fetch repositories for a specific user
def fetch_repositories(user_login):
    check_rate_limit()
    repos = []
    page = 1

    while true:
        response = requests.get(
            f"{GITHUB_API_URL}/users/{user_login}/repos",
            headers=HEADERS,
            params={"sort": "pushed", "page": page, "per_page": 100}
        )
        if response.status_code != 200:
            print(f"Error fetching repositories for {user_login}: {response.status_code}")
            break
        page_repos = response.json()
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1

    return repos

# Fetch users with search criteria
def fetch_users():
    check_rate_limit()
    users = []
    page = 1

    while true:
        response = requests.get(
            f"{GITHUB_API_URL}/search/users",
            headers=HEADERS,
            params={"q": "location:Chicago followers:>100", "page": page, "per_page": 100}
        )
        if response.status_code != 200:
            print(f"Error fetching users: {response.status_code}")
            break
        page_users = response.json().get("items", [])
        if not page_users:
            break
        users.extend(page_users)
        page += 1

    return users

# Save user data to CSV
def save_users(users):
    with open(USERS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["login", "name", "company", "location", "email", "hireable", "bio",
                      "public_repos", "followers", "following", "created_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for user in users:
            user_data = fetch_user_details(user['login'])
            if user_data:
                writer.writerow({
                    "login": user_data.get("login", ""),
                    "name": user_data.get("name", ""),
                    "company": clean_company_name(user_data.get("company")),
                    "location": user_data.get("location", ""),
                    "email": user_data.get("email", ""),
                    "hireable": user_data.get("hireable", ""),
                    "bio": user_data.get("bio", ""),
                    "public_repos": user_data.get("public_repos", 0),
                    "followers": user_data.get("followers", 0),
                    "following": user_data.get("following", 0),
                    "created_at": user_data.get("created_at", "")
                })
    print(f"User data saved to {USERS_CSV}")

# Save repository data to CSV
REPOS_CSV = "repositories.csv"  # Updated file name

def save_repositories(all_repos):
    # Group repositories by user login
    user_repos = defaultdict(list)
    for repo in all_repos:
        user_login = repo["owner"]["login"]
        user_repos[user_login].append(repo)

    with open(REPOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = [
            "login", "full_name", "created_at", "stargazers_count", "watchers_count",
            "language", "has_projects", "has_wiki", "license_name"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each user's repositories
        for login, repos in user_repos.items():
            # Sort repositories by creation date (newest first) and limit to 500
            sorted_repos = sorted(repos, key=lambda repo: repo.get("created_at", ""), reverse=true)[:500]
            
            # Write sorted repositories to CSV
            for repo in sorted_repos:
                writer.writerow({
                    "login": repo["owner"]["login"],
                    "full_name": repo.get("full_name"),
                    "created_at": repo.get("created_at"),
                    "stargazers_count": repo.get("stargazers_count"),
                    "watchers_count": repo.get("watchers_count"),
                    "language": repo.get("language") or "",
                    "has_projects": repo.get("has_projects" or ""),
                    "has_wiki": repo.get("has_wiki" or ""),
                    "license_name": repo.get("license", {}).get("key") if repo.get("license") else ""
                })

    print(f"Repository data saved to {REPOS_CSV}")

# Main function to run the scraper
def main():
    print("Fetching users...")
    users = fetch_users()
    save_users(users)

    all_repos = []
    for user in users:
        print(f"Fetching repositories for {user['login']}...")
        user_repos = fetch_repositories(user['login'])
        all_repos.extend(user_repos)

    save_repositories(all_repos)
    print("Data fetching complete.")

if __name__ == "__main__":
    main()
