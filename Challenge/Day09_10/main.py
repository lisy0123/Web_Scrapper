import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"


def extract_news(url):
	stories = []
	data = requests.get(url).json()
	hits = data["hits"]
	for hit in hits:
		stories.append({
			"title": hit["title"],
			"author": hit["author"],
			"url": hit["url"],
			"objectID": hit["objectID"],
			"points": hit["points"],
			"num_comments": hit["num_comments"]
		})
	return (stories)


def extract_details(url):
	stories = []
	data = requests.get(url).json()
	title = data["title"]
	author = data["author"]
	points = data["points"]
	detail_url = data["url"]
	childrens = data["children"]
	for children in childrens:
		stories.append({
			"author": children["author"],
			"text": children["text"]
		})
	return (stories, title, author, points, detail_url)


db = {}
app = Flask("DayNine")

@app.route("/")
def home():
	word = request.args.get("order_by")
	if word is None:
		word = "popular"
	existing = db.get(word)
	if existing:
		stories = existing
	else:
		if word == "new":
			url = new
		else:
			url = popular
		stories = extract_news(url)
		db[word] = stories
	return render_template("index.html", word = word, stories = stories)


@app.route("/<id>")
def news_id(id):
	url = make_detail_url(id)
	existing = db.get(id)
	if existing:
		stories = existing
		title = db.get(f"{id}_title")
		author = db.get(f"{id}_author")
		points = db.get(f"{id}_points")
		detail_url = db.get(f"{id}_detail_url")
	else:
		stories, title, author, points, detail_url = extract_details(url)
		db[id] = stories
		db[f"{id}_title"] = title
		db[f"{id}_author"] = author
		db[f"{id}_points"] = points
		db[f"{id}_detail_url"] = detail_url
	return render_template(
		"detail.html",
		stories = stories,
		title = title,
		author = author,
		points = points,
		detail_url = detail_url
	)


app.run(host="0.0.0.0")
