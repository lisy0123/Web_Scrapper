import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

def extract(thing):
	try:
		place = thing.find("td", {"class": "local first"}).text.replace("\xa0", " ")
		title = thing.find("span", {"class": "company"}).string
		time = thing.find("td", {"class": "data"}).find("span").string
		pay = thing.find("td", {"class": "pay"}).find("span", {"class": "payIcon"}).string
		pay_sub = thing.find("td", {"class": "pay"}).find("span", {"class": "number"}).string
		date = thing.find("td", {"class": "regDate"}).string
		return {
			"place": place,
			"title": title,
			"time": time,
			"pay": pay+pay_sub,
			"date": date
		}
	except:
		pass


def extract_jobs(job_url):
	jobs = []
	result = requests.get(job_url)
	soup = BeautifulSoup(result.text, "html.parser")
	things = soup.find("tbody").find_all("tr")
	for thing in things:
		job = extract(thing)
		if job is not None:	
			jobs.append(job)
	return (jobs)


def save_to_file(company, jobs):
	company = company.replace("/", ":")
	file = open(f"{company}.csv", mode = "w")
	writer = csv.writer(file)
	writer.writerow(["place", "title", "time", "pay", "date"])
	for job in jobs:
		writer.writerow(list(job.values()))


result = requests.get(alba_url)
soup = BeautifulSoup(result.text, "html.parser")
pages = soup.find_all("li", {"class": "impact"})
for page in pages:
	company = page.find("span", {"class": "company"}).string
	job_url = page.find("a", {"class": "goodsBox-info"})["href"]
	jobs = extract_jobs(job_url)
	save_to_file(company, jobs)
