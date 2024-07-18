import requests
import os

# Set your repository details
OWNER = "your-github-username"
REPO = "vulnerable-python-repo"
HUB_TOKEN = os.getenv("HUB_TOKEN")

# Function to fetch code scanning alerts
def fetch_code_scanning_alerts():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/code-scanning/alerts"
    headers = {"Authorization": f"token {HUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    alerts = response.json()

    high_alerts = [alert for alert in alerts if alert['rule']['severity'] in ['high', 'critical']]
    return high_alerts

# Function to get 'Likelihood of exploitability'
def get_likelihood_of_exploitability(cwe_id):
    url = f"https://cwe.mitre.org/data/definitions/{cwe_id}.html"
    response = requests.get(url)
    if "High" in response.text:
        return "High"
    else:
        return "Not High"

# Fetch alerts and print those with high likelihood of exploitability
high_alerts = fetch_code_scanning_alerts()
for alert in high_alerts:
    cwe_id = alert['rule']['id']
    likelihood = get_likelihood_of_exploitability(cwe_id)
    if likelihood == "High":
        print(f"Vulnerability: {alert['rule']['description']}, Likelihood: {likelihood}")

if __name__ == "__main__":
    fetch_code_scanning_alerts()
