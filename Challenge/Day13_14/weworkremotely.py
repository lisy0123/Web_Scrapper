import requests
from bs4 import BeautifulSoup

def extract_job(html):
	jobs = []
	pages = html.find_all("li")
	for page in pages:
		try:
			html = page.find_all("a")[1]
			title = html.find("span", {"class": "title"}).string
			company = html.find("span", {"class": "company"}).string
			location = html.find("span", {"class": "region company"}).string
			job_id = html['href']
			jobs.append({
				"title": title,
				"company": company,
				"location": location,
				"apply_link": f"https://weworkremotely.com{job_id}"
			})
		except:
			continue
	return (jobs)


def extract_jobs(url):
	jobs = []
	result = requests.get(url)
	soup = BeautifulSoup(result.text, "html.parser")
	results = soup.find_all("section", {"class": "jobs"})
	for result in results:
		job = extract_job(result)
		jobs += job
	return (jobs)


def get_jobs(word):
	url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
	jobs = extract_jobs(url)
	#print("WE: ", len(jobs), url)
	return (jobs)

