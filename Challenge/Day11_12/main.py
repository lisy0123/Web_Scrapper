import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

def scrapping(words):
	things = []
	for word in words:
		result = requests.get(f"https://www.reddit.com/r/{word}/top/?t=month", headers = headers)
		soup = BeautifulSoup(result.text, "html.parser")
		pages = soup.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"}).find_all("div", {"class": "_1poyrkZ7g36PawDueRza-J"})
		for page in pages:
			sub = page.find("a", {"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
			if sub:
				title = page.find("h3", {"class": "_eYtD2XCVieq6emjKBH3m"}).string
				link = sub["href"]
				nums = page.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).string
				if 'k' in nums:
					nums = float(nums[:-1]) * 1000
				elif 'm' in nums:
					nums = float(nums[:-1]) * 1000000
				things.append({
					"title": title,
					"link": link,
					"nums": int(nums),
					"search": word
						})
	return (things)
			

app = Flask("DayEleven")


@app.route("/")
def home():
	return render_template("home.html", subreddits = subreddits)

@app.route("/read")
def read():
	words = request.args
	things = scrapping(words)
	things.sort(key=lambda thing: thing["nums"], reverse=True)
	return render_template("read.html", words = words, things = things)

app.run(host="0.0.0.0")
