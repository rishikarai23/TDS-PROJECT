import pandas as pd

# 1. Top 5 users in Chicago with the highest number of followers
def top_users_by_followers():
    users_df = pd.read_csv('users.csv')
    top_users = users_df.sort_values(by='followers', ascending=False).head(5)
    top_logins = top_users['login'].tolist()
    result = ','.join(top_logins)
    print(result)

# 2. 5 earliest registered GitHub users in Chicago
def earliest_registered_users():
    users_df = pd.read_csv('users.csv')
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])
    earliest_users = users_df.sort_values(by='created_at').head(5)
    earliest_logins = earliest_users['login'].tolist()
    result = ','.join(earliest_logins)
    print(result)

# 3. 3 most popular licenses among users
def top_licenses():
    repositories_df = pd.read_csv('repositories.csv')
    repositories_df = repositories_df[repositories_df['license_name'].notna()]
    license_counts = repositories_df['license_name'].value_counts()
    top_licenses = license_counts.head(3).index.tolist()
    result = ','.join(top_licenses)
    print(result)

# 4. Majority company of developers
def most_common_company():
    users_df = pd.read_csv('users.csv')
    company_counts = users_df['company'].value_counts()
    most_common_company = company_counts.idxmax()
    print(most_common_company)

# 5. Most popular programming language
def most_popular_language():
    repositories_df = pd.read_csv('repositories.csv')
    language_counts = repositories_df['language'].value_counts()
    most_popular_language = language_counts.idxmax()
    print(most_popular_language)

# 6. Second most popular programming language among users who joined after 2020
def second_most_popular_language():
    users_df = pd.read_csv('users.csv')
    repositories_df = pd.read_csv('repositories.csv')
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])
    recent_users = users_df[users_df['created_at'] > '2020-01-01']
    recent_user_logins = recent_users['login'].tolist()
    recent_repositories = repositories_df[repositories_df['login'].isin(recent_user_logins)]
    language_counts = recent_repositories['language'].value_counts()
    second_most_popular_language = language_counts.nlargest(2).index[1]
    print(second_most_popular_language)

# 7. Language with the highest average number of stars per repository
def highest_average_stars_language():
    repositories_df = pd.read_csv('repositories.csv')
    average_stars = repositories_df.groupby('language')['stargazers_count'].mean()
    highest_average_language = average_stars.idxmax()
    print(highest_average_language)

# 8. Top 5 users in terms of leader_strength
def top_leader_strength():
    users_df = pd.read_csv('users.csv')
    users_df['leader_strength'] = users_df['followers'] / (1 + users_df['following'])
    top_leaders = users_df.sort_values(by='leader_strength', ascending=False).head(5)
    top_logins = top_leaders['login'].tolist()
    result = ','.join(top_logins)
    print(result)

# 9. Correlation between followers and public repositories
def correlation_followers_public_repos():
    users_df = pd.read_csv('users.csv')
    correlation = users_df['followers'].corr(users_df['public_repos'])
    print(f"{correlation:.3f}")

# 11. Correlation between having projects and wikis enabled
def correlation_projects_wiki():
    repositories_df = pd.read_csv('repositories.csv')
    correlation = repositories_df['has_projects'].astype(int).corr(repositories_df['has_wiki'].astype(int))
    print(f"{correlation:.3f}")

# 12. Difference in average following between hireable and non-hireable users
def difference_average_following():
    users_df = pd.read_csv('users.csv')
    hireable_users = users_df[users_df['hireable'] == True]
    non_hireable_users = users_df[users_df['hireable'].isna() | (users_df['hireable'] == False)]
    average_hireable_following = hireable_users['following'].mean()
    average_non_hireable_following = non_hireable_users['following'].mean()
    difference = average_hireable_following - average_non_hireable_following
    print(f'Difference in average following (hireable - non-hireable): {difference:.3f}')

# 14. Top 5 users who created the most repositories on weekends
def top_weekend_repo_creators():
    repos_df = pd.read_csv('repositories.csv')
    repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
    weekend_repos = repos_df[repos_df['created_at'].dt.dayofweek.isin([5, 6])]
    top_users = weekend_repos['login'].value_counts().head(5)
    top_users_logins = ','.join(top_users.index)
    print(top_users_logins)

# 15. Do hireable users share their email addresses more often?
def email_sharing_difference():
    users_df = pd.read_csv('users.csv')
    total_users = len(users_df)
    hireable_users = users_df[users_df['hireable'] == True]
    non_hireable_users = users_df[users_df['hireable'].isna() | (users_df['hireable'] == False)]
    fraction_hireable_with_email = hireable_users['email'].notna().mean()
    fraction_non_hireable_with_email = non_hireable_users['email'].notna().mean()
    difference = fraction_hireable_with_email - fraction_non_hireable_with_email
    print(f'{difference:.3f}')

# 16. Most common surname based on user names
def most_common_surname():
    users_df = pd.read_csv('users.csv')
    valid_users = users_df[users_df['name'].notna()]
    valid_users['surname'] = valid_users['name'].str.strip().str.split().str[-1]
    surname_counts = valid_users['surname'].value_counts()
    max_count = surname_counts.max()
    most_common_surnames = surname_counts[surname_counts == max_count].index.tolist()
    most_common_surnames.sort()
    most_common_surnames_str = ', '.join(most_common_surnames)
    print(most_common_surnames_str)

if __name__ == "__main__":
    top_users_by_followers()
    earliest_registered_users()
    top_licenses()
    most_common_company()
    most_popular_language()
    second_most_popular_language()
    highest_average_stars_language()
    top_leader_strength()
    correlation_followers_public_repos()
    correlation_projects_wiki()
    difference_average_following()
    top_weekend_repo_creators()
    email_sharing_difference()
    most_common_surname()
