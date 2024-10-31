# GitHub Data Scraper

## Interesting Findings
1. The top users in Chicago demonstrated a strong presence in JavaScript, which was also the most popular programming language among developers who joined after 2020.
2. Interestingly, despite the number of public repositories, the correlation between followers and repositories was relatively low (0.077), indicating other factors might contribute to follower counts.

## Actionable Recommendations
- Developers should focus on enhancing the quality of their bios, as a longer bio correlates with a higher follower count (slope of 3.048), potentially leading to greater visibility and connections.
- Collaborating on projects with trending programming languages like JavaScript may increase engagement within the developer community, thus fostering networking opportunities.


## Project Overview

This GitHub Data Scraper leverages the GitHub API to gather detailed data about GitHub users and their repositories. The project retrieves user profiles based on specific search criteria and their repositories, saving the information in structured CSV files (`users.csv` and `repositories.csv`). This setup allows for further analysis of GitHub users and repositories, providing insight into user profiles, repository popularity, and maintenance practices.

### Objectives

1. **Data Collection**: Retrieve GitHub user and repository data based on defined parameters (e.g., users from a specific location with followers above a threshold).
2. **Data Analysis**: Structure the data for easy analysis, making it possible to identify trends in user profiles and repository characteristics.
3. **Recommendations**: Provide actionable recommendations to GitHub users and developers based on the analysis.

### Data Scraping Process

The project uses a Python script to interact with the GitHub API, retrieve data, and format it for analysis:

1. **Authentication**: The script authenticates to GitHub using a Personal Access Token (PAT) stored in the `GITHUB_TOKEN` variable to ensure secure API access.
2. **Rate Limiting**: Since the GitHub API has rate limits, the `check_rate_limit` function checks the remaining requests and waits if the rate limit is close to being exhausted.
3. **User Data Retrieval**: Using the `/search/users` endpoint, the script searches for users meeting the criteria specified in `fetch_users()`. It collects user profiles based on location and follower count.
4. **Repository Data Retrieval**: For each user, the `fetch_repositories` function retrieves repository details using the `/users/{username}/repos` endpoint, capturing repository metadata like `stargazers_count`, `language`, and license.
5. **Data Storage**: The script saves the fetched data to CSV files (`users.csv` for user data and `repositories.csv` for repository data) using Python’s `csv` module.

### CSV Output Structure

#### users.csv

Contains information about GitHub users, with the following fields:

- **login**: The user's GitHub username.
- **name**: Full name of the user.
- **company**: The company or organization associated with the user.
- **location**: The geographic location of the user.
- **email**: User's email address, if publicly available.
- **hireable**: Indicates if the user is available for hiring.
- **bio**: A brief biography of the user.
- **public_repos**: The number of public repositories owned by the user.
- **followers**: The number of followers the user has on GitHub.
- **following**: The number of users the user follows on GitHub.
- **created_at**: The date when the user’s GitHub account was created.

#### repositories.csv

Contains information about each user's repositories, with the following fields:

- **login**: The repository owner’s GitHub username.
- **full_name**: The full repository name (owner/repo format).
- **created_at**: The date the repository was created.
- **stargazers_count**: The number of stars the repository has received.
- **watchers_count**: The number of users watching the repository.
- **language**: The main programming language used in the repository.
- **has_projects**: Indicates if the repository has GitHub Projects enabled.
- **has_wiki**: Indicates if the repository has a wiki enabled.
- **license_name**: The license type of the repository, if any.

