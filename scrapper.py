from abc import ABC
from bs4 import BeautifulSoup
import requests
import json

uconfigFile = open('university.config.json')
universityConfig = json.load(uconfigFile)

api_url = 'http://localhost:5000'


class ABCUniversity(ABC):
    def __init__(self, url) -> None:
        self._url = url
        self._page = requests.get(url)
        self._soup = BeautifulSoup(self.content, "html.parser")

    @property
    def url(self):
        return self._url

    @property
    def page(self):
        return self._page

    @property
    def soup(self):
        return self._soup

    @property
    def content(self):
        return self.page.content

    @property
    def courses(self):
        raise NotImplementedError


class UCB(ABCUniversity):

    def __init__(self, url) -> None:
        super().__init__(url)

    def courses(self):
        results = self.soup.find(id='main-wrapper')
        courses = results.find_all("div", class_='content')
        data = []
        for course_element in courses:
            courses_list = course_element.find_all('li')
            for course in courses_list:
                refTag = course.find('a')
                data.append(refTag.text.split('. ')[1])
        return data


def start_scrapper():
    for data in universityConfig:
        scrapper = Scrapper(data)
        scrapper.dumpData()


class Scrapper:
    def __init__(self, data) -> None:
        self.data = data

    # TODO: Implement switch case
    def findCourseScrapper(self, uCode, url):
        if uCode == 'UCB':
            return self.UCB(url)
        elif uCode == 'UIUC':
            return self.UIUC(url)
        elif uCode == 'STU':
            return self.STU(url)

    def UCB(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id='main-wrapper')
        courses = results.find_all("div", class_='content')
        data = []
        for course_element in courses:
            courses_list = course_element.find_all('li')
            for course in courses_list:
                refTag = course.find('a')
                data.append(refTag.text.split('. ')[1])
        return data

    def UIUC(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id='lower5321')
        courses = results.find_all('span')
        data = []
        for course_element in courses:
            # TODO: Add regex to this
            data.append(course_element.text)
        return data

    def STU(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id='courseinventorycontainer')
        courses = results.find_all("div", class_='courseblock')
        data = []
        for course_element in courses:
            course = course_element.find("p", class_='courseblocktitle')
            data.append(course.text.split('. ')[1])
        return data

    def sendData(self, type, data, **kwargs):
        if type == 'university':
            return requests.put(api_url+'/university/', data=data)
        elif type == 'department':
            return requests.put(api_url+'/university/' +
                                kwargs["u_id"]+'/department/', data=data)
        elif type == 'degree':
            return requests.put(api_url+'/university/' +
                                kwargs["u_id"]+'/department/'+kwargs["dept_id"]+'/degree/', data=data)
        elif type == 'course':
            return requests.put(api_url+'/university/'+kwargs["u_id"]+'/department/' +
                                kwargs["dept_id"]+'/degree/'+kwargs["degree_id"]+'/course/', data=data)

    def dumpData(self):
        data = self.data
        universityData = {
            "name": data["details"]["name"],
            "city": data["details"]["city"],
            "state": data["details"]["state"]
        }
        newUniversity = self.sendData(
            "university", universityData, u_id='', dept_id='', degree_id='')
        u_id = newUniversity.json()["data"]["id"]

        for department in data["departments"]:
            departmentData = {
                "name": department["name"],
                "college_name": department["college_name"]
            }
            newDepartment = self.sendData(
                'department', departmentData, u_id=str(u_id), dept_id='', degree_id='')
            dept_id = newDepartment.json()["data"]["id"]
            for degree in department["degrees"]:
                # self.degreeName = degree["name"]
                # self.degreeType = degree["type"]
                degreeData = {
                    "name": degree["name"],
                    "type": degree["type"],
                    "descipline": ""
                }
                newDegree = self.sendData(
                    'degree', degreeData, u_id=str(u_id), dept_id=str(dept_id), degree_id='')
                degree_id = newDegree.json()["data"]["id"]
                courses = self.findCourseScrapper(
                    data["details"]["ucode"], degree["coursesUrl"])
                for course in courses:
                    courseData = {
                        "name": course,
                        "description": "",
                        "code": "",
                        "term": ""
                    }
                    self.sendData('course', courseData, u_id=str(u_id),
                                  dept_id=str(dept_id), degree_id=str(degree_id))


start_scrapper()
