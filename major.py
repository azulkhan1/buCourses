#https://jasper-vulture-314.notion.site/74953ef432014f029743f97f884025ed?v=ec683d332f304a4e873461d48cd79997
import requests
from bs4 import BeautifulSoup

def getPage(url):
    request = requests.get(url)
    if request.status_code != 200:
        return (False, [])
    return (True, request.content)

def getUrls(limit=1):
    base_url = "https://www.bu.edu/academics/cas/courses/computer-science/" + str(limit) #you can change base url depending on major
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

def getUrlsHandler(max_limit=1): #you can change max limit depending on # of courses pages 
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

print(getUrlsHandler(dynamicMaxLimit()[1]))

def getCourseContent(url):
    courseContent = {}
    data = getPage(url)
    if (data[0] == False):
        return (False, [])
    else:
        soup = BeautifulSoup(data[1], 'html.parser')
        h1_elements = soup.find_all('h1')
        course_name = h1_elements[1].text.strip()
        courseContent['courseName'] = course_name

        course_code = soup.h2.text
        courseContent['courseCode'] = course_code

        course_content_div = soup.find('div', id="course-content")
        course_description = course_content_div.find('p').text
        courseContent['courseDiscription'] = course_description

        info_box_div = soup.find('div', id="info-box")
        dd_elements = info_box_div.find_all('dd')
        if len(dd_elements) == 1:
            credit = dd_elements[0].text.strip() 
            prereqs = "None"
            courseContent['credit'] = credit
            courseContent['prereqs'] = prereqs
        else:
            credit = dd_elements[0].text.strip() 
            prereqs = dd_elements[1].text.strip()
            courseContent['credit'] = credit
            courseContent['prereqs'] = prereqs

        offerings_ul = soup.find('ul', class_="cf-hub-offerings")
        if offerings_ul:  
            hubs = [li.text.strip() for li in offerings_ul.find_all('li')]
            num = 1
            for hub in hubs:
                courseContent['hub' + str(num)] = hub
                num += 1
        else:
            hubs = "None"
            courseContent['hub'] = hubs
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
        return (True, all_courses_info[0])
    

#print(getPage("https://www.bu.edu/academics/cas/courses/computer-science/"))
#print(getCourseContent("https://www.bu.edu/academics/cas/courses/cas-cs-112/")) 
#print(getCourseContentHandler(getUrlsHandler())[1])

#To Do:

#put into csv or similar file

#Write script to put it into notion

#--------------------------------------------------------------------------------------

#Potential to expand into university wide scrapper
#https://www.bu.edu/academics/schools-colleges/     link to access each school and through them the course offerings