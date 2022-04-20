import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import re

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

def get_last_JK_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    total_txt = soup.find("strong", {"class": "dev_tot"}).get_text(strip=True)
    total_txt = total_txt.replace(',','')
    total = int(total_txt)
    return (total//20) + 1

def extract_JK(html):
    try:
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
    except:
        return None

def extract_JKs(word):
    url = f"http://www.jobkorea.co.kr/Search/?stext={word}"
    last_page = get_last_JK_page(url)
    jobs = []
    for page in range(last_page):
        print(f"Scrapping JK: Page {page+1}/{last_page}")
        try:   
            result = requests.get(f"{url}&Page_No={page+1}", headers=headers)
        except:
            break
        soup = BeautifulSoup(result.text, "html.parser").find("div", {"class": "list-default"})
        if soup is not None:
            results = soup.find_all("li", {"class": "list-post"})
            for result in results:
                job = extract_JK(result)
                if job:
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
    try:
        parent = html.find("div", {"class": "fl1"})
        title = parent.find("h2").find("a")["title"]
        company, location = parent.find("h3").find_all(
            "span", recursive=False)
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        time = parent.find("ul", {"class": "fs-caption"}).find_all("li")[0].get_text(strip=True)
        job_id = html['data-jobid']
        return {
            'title': title,
            'company': company,
            'location': location,
            'time': time,
            'link': f"https://stackoverflow.com/jobs/{job_id}"
        }
    except:
        return None

def extract_SOs(word):
    url = f"https://stackoverflow.com/jobs?r=true&q={word}"
    last_page = get_last_SO_page(url)
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page {page+1}/{last_page}")
        try:   
            result = requests.get(f"{url}&pg={page+1}", headers=headers)
        except:
            break
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_SO(result)
            if job:
                jobs.append(job)
    return jobs


def extract_WWR(html):
    try:
        parent = html.find("a", {"href": re.compile("/remote-jobs")})
        title = parent.find("span", {"class": "title"}).get_text(strip=True)
        company = parent.find("span", {"class": "company"}).get_text(strip=True)
        location = parent.find("span", {"class": "region"})
        if location is not None:
            location = location.get_text(strip=True)
        else:
            location = "Remote"
        time = parent.find("span", {"class": "date"})
        if time is not None:
            time = time.get_text(strip=True)
        else:
            time = "None"
        
        job_id = parent["href"]
        return {
            'title': title,
            'company': company,
            'location': location,
            'time': time,
            'link': f"https://weworkremotely.com{job_id}"
        }
    except:
        return None

def extract_WWRs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    jobs = []
    print(f"Scrapping WWR")
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    for result in results:
        job = extract_WWR(result)
        if job:
            jobs.append(job)
    return jobs


def get_jobs(word):
    jobs = extract_JKs(word) + extract_SOs(word) + extract_WWRs(word)
    return jobs
