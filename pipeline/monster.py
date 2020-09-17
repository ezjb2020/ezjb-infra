# to reduce load
# we should only craw sites with recency updates
# and only pages that appear that day
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import time
from ez_db import EzDb

db_conn = EzDb()

def bs():
    # url = 'https://www.careerbuilder.com/jobs?posted=1&pay=&cat1=&radius=30&emp=&cb_apply=false&keywords=&location=CA&company_name=&cb_workhome=false'
    url = 'https://www.monster.com/jobs/search/?where=California&rad=20&tm=0'
    response = requests.get(url)
    page_html = response.text
    # print(page_html)
    # cb = 'monster.html'
    # page_html = open(cb)
    soup = BeautifulSoup ( page_html )

    for link in soup.find_all('a'):
        fulllink = link.get ('href')
        print(fulllink)
        # if fulllink and 'https://www.careerbuilder.com/job/' in fulllink:
            # page_url = fulllink.split("=")[1]
            # print(page_url)

def init_mongo_record_schema():
    return {
        'jobTitle': None,
        'industry': None,
        'employmentType': None,
        'description': None,
        'email': None,
        'url': None,
        'createdAt': None,
        'updatedAt': datetime.now(),
        'company': None,
        'location': None,
        'companyLogo': None,
        'source': None
    }

def parse():
    for page in range(8,50):
        url = 'https://www.monster.com/jobs/search/pagination/?where=California&isDynamicPage=true&isMKPagination=true&page=' + str(page) + '&total=26'
        response = requests.get(url)
        page_json = response.text
        data = json.loads(page_json)

        visited_list = db_conn.get_sources()
        for obj in data:
            # print(obj)
            if 'Title' in obj:
                source = obj['TitleLink']
                print(source)

                if source in visited_list:
                    continue
                visited_list.append(source)
                jobTitle = obj['Title']
                print(jobTitle)
                location = obj['LocationText']
                print(location)
                createdAt = datetime.strptime(obj['DatePosted'], '%Y-%m-%dT%H:%M')
                print(createdAt)
                if obj['Company'] and obj['Company']['Name']:
                    company = obj['Company']['Name']
                    print(company)
                if 'CompanyLogoUrl' in obj:
                    companyLogo = obj['CompanyLogoUrl']
                    if companyLogo[0:2] == '//':
                        companyLogo = 'https:' + companyLogo
                    print(companyLogo)
                # 'url': None,

                page_data = parse_single_page(source)

                print()
                mongo_obj =  {
                    'jobTitle': jobTitle,
                    'industry': page_data['industry'],
                    'employmentType': page_data['employmentType'],
                    'description': page_data['description'],
                    'email': None,
                    'url': page_data['url'],
                    'createdAt': createdAt,
                    'updatedAt': datetime.now(),
                    'company': company,
                    'location': location,
                    'companyLogo': companyLogo,
                    'source': source
                }
                db_conn.create_post(mongo_obj)

                time.sleep(1)

# returns
#   'description': description,
#   'employmentType': employmentType,
#   'industry': industry,
#   'url': url,
def parse_single_page(url):
    response = requests.get(url)
    page_html = response.text
    # print(page_html)
    # cb = 'monster_page.html'
    # page_html = open(cb)
    soup = BeautifulSoup ( page_html )

    content = soup.find('script',{"name":"redux_preload"}).contents[0]
    data = json.loads(content.split('window.__INITIAL_STATE__ = ')[1])
    job = data['job']
    description = job['description']
    try:
        url = job['extensions']['apply']['applyOnlineUrl']
    except:
        url = None
    # if job['extensions'] and job['extensions']['inferredData']:
        # niches = job['extensions']['inferredData']['niches']
        # rankedSkills = job['extensions']['inferredData']['rankedSkills']
    try:
        for idx, data in enumerate(soup.find(text='Job Type:  ').parent.parent.children):
            if idx == 3:
                employmentType = data.text
    except:
        employmentType = None

    try:
        for idx, data in enumerate(soup.find(text='Job:  ').parent.parent.children):
            if idx == 3:
                industry = data.text
    except:
        industry = None

    return {
        'description': description,
        'employmentType': employmentType,
        'industry': industry,
        'url': url,
        # niches: niches,
        # rankedSkills: rankedSkills
    }

parse()
