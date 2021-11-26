import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():
	result = requests.get(URL)
	soup = BeautifulSoup(result.text, "html.parser")
	pagination = soup.find("ul", {"class": "pagination-list"})
	links = pagination.find_all('a')
	pages = []

	for link in links[:-1]:
	  pages.append(int(link.string))
	max_page = pages[-1]
	return (max_page)


def extract_job(html):
	jobtitle = html.find("h2", {"class": "jobTitle"})
	title = jobtitle.find("span").string
	if title == "new":
		title = jobtitle.find_all("span")[1].string
	company = html.find("span", {"class": "companyName"})
	if company:
		if company.find("a") is not None:
			company = company.find("a").string
		else:
			company = company.string
	else:
		company = None
	location = html.find("div", {"class": "companyLocation"}).text
	job_id = html.parent["data-jk"]
	return {
		"title": title,
		"comapny": company,
		"location": location,
		"link": f"https://www.indeed.com/viewjob?jk={job_id}"
	}


def extract_jobs(last_page):
	jobs = []
	for page in range(last_page):
		print(f"Scrapping Indeed: Page: {page}")
		result = requests.get(f"{URL}&start={page*LIMIT}")
		soup = BeautifulSoup(result.text, "html.parser")
		results = soup.find_all("div", {"class": "slider_container"})
		for result in results:
			job = extract_job(result)
			jobs.append(job)
	return (jobs)


def get_jobs():
	last_page = get_last_page()
	jobs = extract_jobs(last_page)
	return (jobs)
