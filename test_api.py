import urllib.request
import os

url = "https://api.github.com/repos/facebook/react/pulls/30000"
headers = {
    "Accept": "application/vnd.github.v3.diff",
    "User-Agent": "Mozilla/5.0"
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    print(response.read().decode("utf-8")[:200])
