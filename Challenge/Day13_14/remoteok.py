import requests
from bs4 import BeautifulSoup

def extract_job(html):
	title = html.find("h3", {"itemprop": "name"}).string
	company = html.find("h2", {"itemprop": "title"}).string
	try:
		location = html.find("div", {"class": "location tooltip"}).string
	except:
		location = ""
	job_id = html['data-url']
	return {
		"title": title,
		"company": company,
		"location": location,
		"apply_link": f"https://remoteok.io{job_id}"
	}


def extract_jobs(url):
	jobs= []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
	result = requests.get(url, headers=headers)
	soup = BeautifulSoup(result.text, "html.parser")
	results = soup.find_all("tr", {"class": "job"})
	for result in results:
		job = extract_job(result)
		jobs.append(job)
	return (jobs)


def get_jobs(word):
	url = f"https://remoteok.io/remote-{word}-jobs"
	jobs = extract_jobs(url)
	#print("RE: ", len(jobs), url)
	return (jobs)

