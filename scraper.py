#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7
from bs4 import BeautifulSoup
import urllib3
import requests
import time
import re
import csv
from csv import DictReader

URL = "https://www.lsa.umich.edu/cg/cg_results.aspx?termArray=f_20_2310&cgtype=ug&show=200&numlvl=300&numlvl=400&department=EECS"

r = requests.get(URL)
#test
soup = BeautifulSoup(r.content, 'html5lib')

courses = []

container = soup.find('div', attrs = {'id':'container'})
container = soup.find('div', attrs = {'id':'contentMain_panelResults'})
for course_entry in container.findAll('div', attrs = {'class':'row toppadding_main bottompadding_interior'}):
    course = {}
    course['name'] = (" ".join(course_entry.font.get_text().split())).replace('"','')
    course['url'] = "https://www.lsa.umich.edu/cg/" + course_entry.a['href']
    if(len(courses)==0 or courses[len(courses)-1]['name']!=course['name']):
        courses.append(course)


for eecs_class in courses:
    lec_seats, lab_seats, disc_seats, sem_seats, WL_seats = 0,0,0,0,0
    r_indiv = requests.get(eecs_class['url'])
    print(eecs_class['name'])
    soup = BeautifulSoup(r_indiv.content,'html5lib')
    for row in soup.findAll('div', attrs = {'class':'row clsschedulerow toppadding_main bottompadding_main'}):
        col_cont = row.find('div', {'class':'col-md-12'})
        cols = col_cont.findAll('div', {'class':'col-md-1'})
        class_type = cols[0].find('span')
        seats = 0
        if class_type:
                if re.search(r'\(LAB\)',class_type.get_text()):
                    print("this is a lab")
                    try:
                        seats = int(re.search(r'(\d+)',cols[4].get_text()).group(1))
                    except AttributeError:
                        seats = 0
                    print(seats)
                    lab_seats += seats
                elif re.search(r'\(DIS\)',class_type.get_text()):
                    print("this is a disc")
                    try:
                        seats = int(re.search(r'(\d+)',cols[4].get_text()).group(1))
                    except AttributeError:
                        seats = 0
                    print(seats)
                    disc_seats += seats
                    try:
                        WL = int(re.search(r'(\d+)',cols[5].get_text()).group(1))
                    except AttributeError:
                        WL = 0
                    print(WL)
                    WL_seats += WL
                elif re.search(r'\(LEC\)',class_type.get_text()):
                    print("this is a lec")
                    try:
                        seats = int(re.search(r'(\d+)',cols[4].get_text()).group(1))
                    except AttributeError:
                        seats = 0
                    print(seats)
                    lec_seats += seats
                    try:
                        WL = int(re.search(r'(\d+)',cols[5].get_text()).group(1))
                    except AttributeError:
                        WL = 0
                    print(WL)
                    WL_seats += WL
                elif re.search(r'\(SEM\)',class_type.get_text()):
                    print("this is a sem")
                    try:
                        seats = int(re.search(r'(\d+)',cols[4].get_text()).group(1))
                    except AttributeError:
                        seats = 0
                    print(seats)
                    sem_seats += seats
                    try:
                        WL = int(re.search(r'(\d+)',cols[5].get_text()).group(1))
                    except AttributeError:
                        WL = 0
                    print(WL)
                    WL_seats += WL

    eecs_class['ts'] = time.time()
    eecs_class['lab_seats'] = lab_seats
    eecs_class['disc_seats'] = disc_seats
    eecs_class['lec_seats'] = lec_seats
    eecs_class['sem_seats'] = sem_seats
    eecs_class['WL'] = WL_seats

csv_file = '/Users/willsoltas/Desktop/Dev/EECScheduler/EECScheduler/EECSUL_f2020.csv'
for course in courses:
    try:
        del course['url']
    except KeyError:
        print("Key 'url' not found")

with open(csv_file, 'r') as f: 
        r = csv.DictReader(f)
        for i, line in enumerate(r):
            if i >= 59:
                break
            if i >=1:
                print(i)
                print(line)
                courses[i]['min_indx'] = dict(line).get('min_indx')

for course in courses:
    min_indx_str = course.get('min_indx')
    if min_indx_str == 'null' or course.get(min_indx_str) == 0:
        course['Open'] = 0
    else:
        course['Open'] = 1

csv_cols = ['name', 'ts', 'lec_seats', 'lab_seats', 'disc_seats', 'sem_seats', 'WL', 'min_indx', 'Open']
with open(csv_file, 'a') as db:
    writer = csv.DictWriter(db, fieldnames=csv_cols)
    for data in courses:
            writer.writerow(data)



