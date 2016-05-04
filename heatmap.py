import lxml.html

root = 'http://registrar.sas.cornell.edu/courses/roster/FA14/'

def parse_dept(url):
    """ Extracts the subcourses from the given department.

    Arguments:
    url is the Cornell course roster link to the department.

    Return values:
    subcourse_list is a list of all the subcourses.
    """

    x = lxml.html.parse(url)
    course_roots = x.xpath('//*[@class="course"]')

    subcourse_list = []

    for course_root in course_roots:

        day_elems = course_root.xpath('div//*[@class="mtgpat"]')
        time_elems = course_root.xpath('div//*[@class="mtg_time"]')

        for j in range(0, len(day_elems)):

            if day_elems[j].text == u'\xa0' or 'TBA' in day_elems[j].text:
                day_list = []
            else:
                day_list = convert_day(day_elems[j].text)
            if time_elems[j].text == u'\xa0' or 'TBA' in time_elems[j].text:
                hour_list = []
            else:
                hour_list = convert_time(time_elems[j].text)

            subcourse = [day_list, hour_list]
            subcourse_list.append(subcourse)

    return subcourse_list

def convert_day(day):
    """ Converts day strings to day lists.

    Arguments:
    day is the day string (e.g. 'TR')

    Return values:
    day_list is the list of days (e.g. [1, 3])
    """

    day_list = []

    if 'M' in day:
        day_list.append(1)
    if 'T' in day:
        day_list.append(2)
    if 'W' in day:
        day_list.append(3)
    if 'R' in day:
        day_list.append(4)
    if 'F' in day:
        day_list.append(5)
    if 'S' in day:
        day_list.append(6)
    if 'U' in day:
        day_list.append(7)

    return day_list

def convert_time(time):
    """ Converts time strings to hour lists.

    Arguments:
    time is the time string (e.g. '10:10AM  - 11:25AM')

    Return values:
    hour_list is the list of hours (e.g. [10, 11])
    """

    s = time.split()[0]
    s_h = int(s.split(':')[0])

    am_pm = s.split(':')[1][-2:]
    if s_h == 12:
        s_h = s_h - 12
    if am_pm == 'PM':
        s_h = s_h + 12
    s_h = s_h + 1

    e = time.split()[2]
    e_h = int(e.split(':')[0])

    am_pm = e.split(':')[1][-2:]
    if e_h == 12:
        e_h = e_h - 12
    if am_pm == 'PM':
        e_h = e_h + 12
    e_h = e_h + 1

    hour_list = range(s_h, e_h + 1)
    return hour_list

def dept_to_tsv(subcourse_list, name):
    """ Converts a subcourse_list to a .tsv heatmap file.

    Arguments:
    subcourse_list is a list of all the subcourses in a department.
    name is the name of that department.
    """

    tsv_file = name.split(':')[0] + '.tsv'
    f = open(tsv_file, 'w+')
    f.write('day\thour\tvalue\n')

    d = {}

    for day in range(1, 7 + 1):
        for hour in range(1, 24 + 1):
            d[(day, hour)] = 0

    for subcourse in subcourse_list:
        for day in subcourse[0]:
            for hour in subcourse[1]:
                d[(day, hour)] = d[(day, hour)] + 1

    for key, value in d.items():
        day, hour = key
        f.write(str(day) + '\t' + str(hour) + '\t' + str(value) + '\n')

    f.close()

x = lxml.html.parse(root)
urls = x.xpath('//div/span/a/@href')
subcourse_list = []

for url in urls:
    full_url = root + url
    subcourse_list = subcourse_list + parse_dept(full_url)

dept_to_tsv(subcourse_list, 'ALL_DEPARTMENTS')
