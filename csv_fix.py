import csv
from csv import DictReader

csv_file = '/Users/willsoltas/Desktop/Dev/EECScheduler/EECScheduler/EECSUL_f2020.csv'
csv_new = '/Users/willsoltas/Desktop/Dev/EECScheduler/EECScheduler/EECSUL_f2020--new.csv'
with open(csv_file, 'r') as i:
    dict_reader = DictReader(i)
    courses = list(dict_reader)

new_course_list = []
for course in courses:
    new_course = dict(course)
    new_course['WL'] = 0
    restrict_arr = [int(new_course['lab_seats']),int(new_course['disc_seats']),int(new_course['lec_seats']),int(new_course['sem_seats'])]
    try:
        m = min(i for i in restrict_arr if i > 0)
        m = restrict_arr.index(m)
        ky = ""
        if m == 0:
            ky = 'lab_seats'
        elif m == 1:
            ky = 'disc_seats'
        elif m==2:
            ky = 'lec_seats'
        elif m==3:
            ky = 'sem_seats'
        new_course['min_indx'] = ky
    except ValueError:
        ky = 'null'
        new_course['min_indx'] = ky
    #list(course)[m]==0:
    if new_course.get('min_indx') == 'null':
        new_course['Open'] = 0
    else:
        new_course['Open'] = 1
    print(new_course)
    new_course_list.append(new_course)


csv_cols = ['name', 'ts', 'lec_seats', 'lab_seats', 'disc_seats', 'sem_seats', 'WL', 'min_indx', 'Open']
with open(csv_new, 'w') as db:
    writer = csv.DictWriter(db, fieldnames=csv_cols)
    for data in new_course_list:
            writer.writerow(data)

