import requests
from bs4 import BeautifulSoup
import re


def get_last_JK_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    total_txt = soup.find("strong", {"class": "dev_tot"}).get_text(strip=True)
    total = int(total_txt)
    return (total//20) + 1

def extract_JK(html):
    title = html.find("a", {"class": "title dev_view"}).get_text(strip=True)
    company = html.find("a", {"class": "name dev_view"}).get_text(strip=True)
    location = html.find("span", {"class": "loc long"}).get_text(strip=True)
    time = html.find("span", {"class": "date"}).get_text(strip=True)
    job_id = html['data-gno']
    return {
        'title': title,
        'company': company,
        'location': location,
        'time' : time,
        'link': f"http://www.jobkorea.co.kr/Recruit/GI_Read/{job_id}"
    }

def extract_JKs(word):
    url = f"http://www.jobkorea.co.kr/Search/?stext={word}"
    last_page = get_last_JK_page(url)
    jobs = []
    for page in range(last_page):
        print(f"Scrapping JK: Page {page+1}/{last_page}")
        result = requests.get(f"{url}&Page_No={page+1}")
        soup = BeautifulSoup(result.text, "html.parser").find("div", {"class": "list-default"})
        if soup is not None:
            results = soup.find_all("li", {"class": "list-post"})
            for result in results:
                job = extract_JK(result)
                jobs.append(job)
    return jobs


def get_last_SO_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    if pagination == None:
        return 1
    else:
        pages = pagination.find_all("a")
        last_page = pages[-2].get_text(strip=True)
        return int(last_page)

def extract_SO(html):
    parent = html.find("div", {"class": "fl1"})
    title = parent.find("h2").find("a")["title"]
    company, location = parent.find("h3").find_all(
        "span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    time = parent.find("div", {"class": "fs-caption"}).find_all("div", {"class": "grid--cell"})[0].get_text(strip=True)
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        'time': time,
        'link': f"https://stackoverflow.com/jobs/{job_id}"
    }

def extract_SOs(word):
    url = f"https://stackoverflow.com/jobs?r=true&q={word}"
    last_page = get_last_SO_page(url)
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page {page+1}/{last_page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_SO(result)
            jobs.append(job)
    return jobs


def extract_WWR(html):
    parent = html.find("a", {"href": re.compile("/remote-jobs")})
    spans = parent.find_all("span")
    company = spans[0].get_text(strip=True)
    location = parent.find("span", {"class": "region company"}).get_text(strip=True)
    time = parent.find("span", {"class": "date"}).get_text(strip=True)
    title = spans[1].get_text(strip=True)
    job_id = parent["href"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'time': time,
        'link': f"https://weworkremotely.com{job_id}"
    }

def extract_WWRs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    jobs = []
    print(f"Scrapping WWR")
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    for result in results:
        job = extract_WWR(result)
        jobs.append(job)
    return jobs


def get_jobs(word):
    jobs = extract_JKs(word) + extract_SOs(word) + extract_WWRs(word)
    return jobs
