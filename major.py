#https://jasper-vulture-314.notion.site/74953ef432014f029743f97f884025ed?v=ec683d332f304a4e873461d48cd79997
import requests
from bs4 import BeautifulSoup

#request = requests.get("https://www.bu.edu/academics/cas/courses/computer-science/")
#print(request.content)
#soup = BeautifulSoup(html_doc, 'html.parser')

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

def getUrlsHandler(maxLimit=4): #you can change max limit depending on # of courses pages 
    limit = 1
    links_array = []
    while limit <= maxLimit:
        if (getUrls(limit) == (False, [])):
            return (False, [])
        else:
            data = getUrls(limit)
            links_array += data[1]
        limit += 1
    return (True, links_array)

def getCourseContent(url):
    #courseContent= {}
    data = getPage(url)
    if (data[0] == False):
        return (False, [])
    else:
        soup = BeautifulSoup(data[1], 'html.parser')
        h1_elements = soup.find_all('h1')
        course_name = h1_elements[1].text.strip()
        course_code = soup.h2.text
        course_content_div = soup.find('div', id="course-content")
        course_description = course_content_div.find('p').text
        info_box_div = soup.find('div', id="info-box")
        dd_elements = info_box_div.find_all('dd')
        if len(dd_elements) == 1:
            credit = dd_elements[0].text.strip() 
            prereqs = "None"
        else:
            credit = dd_elements[0].text.strip() 
            prereqs = dd_elements[1].text.strip()
            return prereqs
        #return course_name

# def getCourseContentHandler(urls):
    

#print(getPage("https://www.bu.edu/academics/cas/courses/computer-science/"))
print(getCourseContent("https://www.bu.edu/academics/cas/courses/cas-cs-132/")) 
#print(getUrlsHandler())

#To Do:

#Get pre-reqs if any

#Get Hubs if any

#put into csv or similar file

#Write script to put it into notion

#--------------------------------------------------------------------------------------

#Potential to expand into university wide scrapper
#https://www.bu.edu/academics/schools-colleges/     link to access each school and through them the course offerings