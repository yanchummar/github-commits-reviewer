import requests
from urllib.parse import urlparse
from openai import OpenAI

from prompts import REVIEW_SYSTEM_PROMPT
from config import GITHUB_ACCESS_TOKEN

client = OpenAI()

sus_repos = []

def get_commits(username, repo_name):
  url = f'https://api.github.com/repos/{username}/{repo_name}/commits'
  headers = {'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    commits = response.json()
    return commits
  else:
    print(f"Error: Unable to fetch commits. Status code: {response.content}")
    return None

def extract_repo_info(repo_url):
  parsed_url = urlparse(repo_url)
  path_parts = parsed_url.path.split('/')
  
  if len(path_parts) == 3:  # Check if the path has the expected format (/user/repo)
    return path_parts[1], path_parts[2]
  else:
    print(f"Invalid GitHub repository URL: {repo_url}")
    return None, None
  
# create a function to review github commit messages using gpt3.5
def is_commits_suspicious(commit_message):
  # create a list of commit messages
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.2,
    messages=[
      { "role": "system", "content": REVIEW_SYSTEM_PROMPT % commit_message },
      { "role": "user", "content": "START" }
    ]
  )

  return completion.choices[0].message.content

# Replace 'your-github-urls.txt' with the path to a text file containing a list of GitHub repository URLs (one per line)
with open('github-repos.txt', 'r') as file:
  repo_urls = [line.strip() for line in file]

for repo_url in repo_urls:
  username, repo_name = extract_repo_info(repo_url)

  if username and repo_name:
    # print(f"\nRepository: {username}/{repo_name}")x

    commits = get_commits(username, repo_name)
    if commits:
      # print(f"Number of commits: {len(commits)}")
      
      # combine all commit messages into a single string with numbering for each commit
      commit_messages = '\n'.join([f"{i+1}. {commit['commit']['message']}" for i, commit in enumerate(commits)])
      is_sus_commits = is_commits_suspicious(commit_messages)

      if len(commits) < 5 or 'True' in is_sus_commits:
        sus_repos.append((repo_url, len(commits)))
    else:
      print("Failed to retrieve commits.")
  else:
    print("Invalid GitHub repository URL.")

print("\n\nSuspicious repositories:")
for repo_url in sus_repos:
  print(f'{repo_url[0]} ({repo_url[1]} commits)')
