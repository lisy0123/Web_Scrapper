from flask import Flask, render_template, request, redirect, send_file
from exporter import save_to_file
from stackoverflow import get_jobs as stack_jobs
from weworkremotely import get_jobs as wework_jobs
from remoteok import get_jobs as remoteok_jobs

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
	return render_template("home.html")


@app.route("/report")
def report():
	word = request.args.get('word')
	if word:
		word = word.lower()
		existingJobs = db.get(word)
		if existingJobs:
			jobs = existingJobs
		else:
			jobs = wework_jobs(word) + remoteok_jobs(word) + stack_jobs(word)
			db[word] = jobs	
	else:
		return redirect("/")
	return render_template(
		"report.html",
		search = word,
		nums = len(jobs),
		jobs = jobs
	)


@app.route("/export")
def export():
	try:
		word = request.args.get("word")
		if not word:
			raise Exception()
		word = word.lower()
		jobs = db.get(word)
		if not jobs:
			raise Exception()
		save_to_file(jobs)
		return send_file("jobs.csv")
	except:
		return redirect("/")


app.run(host="0.0.0.0")
