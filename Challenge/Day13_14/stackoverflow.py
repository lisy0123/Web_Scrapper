import requests
from bs4 import BeautifulSoup

def extract_job(html):
	title = html.find("h2", {"class": "mb4"}).find("a")["title"]
	company, location = html.find("h3", {"class": "mb4"}).find_all("span", recursive = False)
	company = company.get_text(strip = True)
	location = location.get_text(strip = True)
	job_id = html['data-jobid']
	return {
		"title": title,
		"company": company,
		"location": location,
		"apply_link": f"https://stackoverflow.com/jobs/{job_id}"
	}


def extract_jobs(url, last_page):
	jobs= []
	for page in range(1, last_page+1):
		#print(f"Scrapping SO: {page}")
		result = requests.get(f"{url}&pg={page}")
		soup = BeautifulSoup(result.text, "html.parser")
		results = soup.find_all("div", {"class": "-job"})
		for result in results:
			job = extract_job(result)
			jobs.append(job)
	return (jobs)


def get_last_page(url):
	result = requests.get(url)
	soup = BeautifulSoup(result.text, "html.parser")
	if soup.find("p", {"class": "ws-pre-wrap"}):
		return (0)
	else:
		try:
			pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
			last_page = pages[-2].get_text(strip = True)
			return (int(last_page))
		except:
			return (1)


def get_jobs(word):
	url = f"https://stackoverflow.com/jobs?r=True&q={word}"
	last_page = get_last_page(url)
	if last_page == 0:
		#print("SO: 0", url)
		return ([])
	else:
		jobs = extract_jobs(url, last_page)
		#print("SO: ", len(jobs), url)
		return (jobs)
