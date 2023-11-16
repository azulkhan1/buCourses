import requests
from bs4 import BeautifulSoup

def getPage(url):
    request = requests.get(url)
    if request.status_code != 200:
        return (False, [])
    return (True, request.content)

def getUrls(limit=1):
    base_url = "https://www.bu.edu/academics/cas/courses/computer-science/" + str(limit) 
    data = getPage(base_url)

    if (data[0] == False):
        return (False, [])
    else:
        soup = BeautifulSoup(data[1], 'html.parser')
        course_feed = soup.find('ul', class_="course-feed") 
        if course_feed:
            links = [li.find('a')['href'] for li in course_feed.find_all('li') if li.find('a')]
            return (True, links)
        else:
            return (False, [])

def dynamicMaxLimit():
    max_limit = 1
    while True: 
        base_url = "https://www.bu.edu/academics/cas/courses/computer-science/" + str(max_limit)
        data = getPage(base_url)
        if (data[0] == False):
            return (False, [])
        else:
            soup = BeautifulSoup(data[1], 'html.parser')
            course_feed = soup.find('ul', class_="course-feed") 
            if course_feed and course_feed.find_all('li'):
                max_limit += 1
            else:
                max_limit -= 1
                break
    return (True, max_limit)

def getUrlsHandler(max_limit=1): 
    limit = 1
    links_array = []
    while limit <= max_limit:
        if (getUrls(limit) == (False, [])):
            return (False, [])
        else:
            data = getUrls(limit)
            links_array += data[1]
        limit += 1
    return (True, links_array)

def getCourseContent(url):
    courseContent = {}
    data = getPage(url)
    if (data[0] == False):
        return (False, [])
    else:
        soup = BeautifulSoup(data[1], 'html.parser')
        course_code = soup.h2.text
        courseContent['courseCode'] = course_code

        h1_elements = soup.find_all('h1')
        course_name = h1_elements[1].text.strip()
        courseContent['courseName'] = course_name

        offerings_ul = soup.find('ul', class_="cf-hub-offerings")
        if offerings_ul:  
            bu_hubs = [li.text.strip() for li in offerings_ul.find_all('li')]
            hubs = ""
            for hub in bu_hubs:
                hubs += " " +hub
            courseContent['hub(s)'] = hubs
        else:
            hubs = "None"
            courseContent['hub(s)'] = hubs

        info_box_div = soup.find('div', id="info-box")
        dd_elements = info_box_div.find_all('dd')
        if len(dd_elements) == 1:
            credit = dd_elements[0].text.strip() 
            prereqs = "None"
            courseContent['prereqs'] = prereqs
            courseContent['credit'] = credit
        else:
            credit = dd_elements[0].text.strip() 
            prereqs = dd_elements[1].text.strip()
            courseContent['prereqs'] = prereqs
            courseContent['credit'] = credit

        return (True, courseContent)

def getCourseContentHandler(urls):
    if urls[0] == False:
        return (False, [])
    else:
        course_links = urls[1]
        all_courses_info = []
        for link in course_links:
            base_url = "https://www.bu.edu/"
            course_info = getCourseContent(base_url + link)
            if course_info[0] == False:
                return (False, [])
            else:
               all_courses_info.append(course_info[1])
        return (True, all_courses_info)
