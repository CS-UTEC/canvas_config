import datetime
import canvas
import re
import pandas as pd


from datetime import timedelta
import json

#####################################################################################################
#courses               = ['5396','5487','5250', '5251']   # From Canvas
#courses               = ['5335','5338','5569']   # From Canvas
first_week           = int(input("Week from: "))        # from this week
last_week            = int(input("Week to  : "))        # until this week

def get_course_name(course_details):
    big_name = course_details['name']
    parts = big_name.split("-")
    name = re.sub("\([A-Z0-9]{6,}\)","", parts[0])
    return name.strip()

def check_expression(regex, text):
    x = re.match(regex, text)
    if x != None :
        return True

def check_name(part, name):
    regex = "^(2020-II) [A-Z0-9]{6,} (ES|EN) ("+name+")$"
    return check_expression(regex, part)

def check_record_name(part, name):
    regex = "^Grabación (2020-II) [A-Z0-9]{6,} (ES|EN) ("+name+")$"
    return check_expression(regex, part)

def check_section(part):
    regex = "^\d+([.]\d+)?$"
    return check_expression(regex, part)

def check_week(part):
    regex = "^Semana[0-9]{2,}$"
    return check_expression(regex, part)

def check_professor(part):
    regex = r"^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$"
    return check_expression(regex, part)

def check_date(part):
    regex = "^\d\d/\d\d$"
    return check_expression(regex, part)

def check_hour(part):
    regex = "^\d\d\:\d\d\ ?-\ ?\d\d\:\d\d\,? (Teoría)|(Laboratorio)$"
    return check_expression(regex, part)


def check_url(part):
    regex = "^https://utec.zoom.us/"
    return check_expression(regex, part)

def check_published(part):
    return part

def check_recordings(week, course, module, item, name):
    parts =  re.split(',', item['title'])
    isNameOK  = False
    try:
        t1 = check_record_name(parts[0].strip(), name)
        t2 = check_section(parts[1].strip())
        t3 = check_week(parts[2].strip())
        t4 = check_professor(parts[3].strip())
        t5 = check_date(parts[4].strip())
        t6 = check_hour(parts[5].strip())
        isNameOK = t1 and t2 and t3 and t4 and t5 and t6
    except Exception as e:
        isNameOK = False

    isUrlOK = check_url(item['external_url'].strip())
    isPublished = check_published(item['published'])
    row = {'Course': course, 'Week':week, 'Type':'Recording', 'isTitleOK':isNameOK, 'isURLOK':isUrlOK, 'isPublished':isPublished, 'Title':item['title'], 'URL':item['external_url'] }
    return row

def check_videoconferencia(week, course, module, item, name):
    parts =  re.split(',', item['title'])
    isNameOK  = False
    try:
        t1 = check_name(parts[0].strip(), name)
        t2 = check_section(parts[1].strip())
        t3 = check_week(parts[2].strip())
        t4 = check_professor(parts[3].strip())
        t5 = check_date(parts[4].strip())
        t6 = check_hour(parts[5].strip())
        isNameOK = t1 and t2 and t3 and t4 and t5 and t6
    except Exception as e:
        isNameOK = False
    isUrlOK = check_url(item['external_url'].strip())
    isPublished = check_published(item['published'])
    row = {'Course': course,'Week':week, 'Type':'Videoconf', 'isTitleOK':isNameOK, 'isURLOK':isUrlOK, 'isPublished':isPublished, 'Title':item['title'], 'URL':item['external_url'] }
    return row

def check(course):
    print("Reviewing...", course)
    week = 0
    course_details = canvas.get_course(course)
    #print(course_details)
    canvas_course_name = get_course_name(course_details)
    df = pd.DataFrame(columns=['Course','Week', 'Type', 'isTitleOK','isURLOK','isPublished', 'Title', 'URL'])

    for module in  canvas.get_modules(course):
        if module['name'].startswith('Semana '):
            #print(module)
            week += 1
            if week >= first_week and week <= last_week :
                print("Scanning week",week)
                items = canvas.get_items(course, module['id'])
                for item in items:
                    if item['type'] == 'ExternalUrl':
                        if item['external_url'].startswith('https://utec.zoom.us/rec/'):
                            r = check_recordings(week, course, module['id'], item, canvas_course_name)
                            df = df.append(r,ignore_index=True)
                        elif item['external_url'].startswith('https://utec.zoom.us/'):
                            r = check_videoconferencia(week,course, module['id'], item, canvas_course_name)
                            df = df.append(r, ignore_index=True)
    return df

result = pd.DataFrame(columns=['Course','Week', 'Type', 'isTitleOK','isURLOK','isPublished', 'Title', 'URL'])

filepath = 'courses.txt'
with open(filepath) as f:
    lines = [line.rstrip() for line in f]
    for course in lines:
        df_course = check(course)
        result = result.append(df_course, ignore_index=True)

result.to_csv(r'result.csv', index = False)
