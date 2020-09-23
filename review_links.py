import datetime
import canvas
import re

from datetime import timedelta
import json

#####################################################################################################
#                                   Just config your course here                                    #
course               = '0000'   # From Canvas
course_cod           = 'CS2901' # From our curricula at the university
course_name          = 'Ingeniería de Software 1'
course_section       = '1' #CURSO-SECCIÓN
course_professor     = 'Jesus Bellido'
course_type          = 'Teoría' #"TIPO [Teoría|Labotorio]:")
course_starts        = '19:00'  #input("HORA INICIO: HH:mm ")
course_ends          = '20:00'  #input("HORA FIN: HH:mm ")
dia                  = 3        #primer día de clases en Abril.
zoom_url             = 'https://invalid'       #input("LINK ZOOM:")
first_week           = 1        # from this week
last_week            = 17        # until this week

print('===========================================================')
print('Revisar https://utec.instructure.com/profile/settings      ')
print('Entrar en Integraciones aprobadas -> +Nuevo Token de Acceso')

is_visible_videoconf = False # Add label for Videoconferencia
is_visible_headers   = False # Add labels for Mayterial de Clase & Actividades
is_visible_recordings   = False
is_visible_links     = False # Create links for Videoconferencia and Grabacion

#####################################################################################################
#CONNECTOR



def configure_week(module_id, date):

    date_start = date - timedelta(days=date.weekday())
    date_end = date_start + timedelta(days=6)
    #items = get_items(course, module['id'])
    if is_visible_videoconf:
        h = "Videoconferencia - Semana <start_mes>/<start_dia> - <end_mes>/<end_dia>"
        h = h.replace('<start_dia>',date_start.strftime("%d") )
        h = h.replace('<start_mes>',date_start.strftime("%m") )
        h = h.replace('<end_dia>',date_end.strftime("%d") )
        h = h.replace('<end_mes>',date_end.strftime("%m") )
        create_header(course, module_id, h)
    if is_visible_recordings:
        create_header(course, module_id, 'Grabaciones')
    if is_visible_headers:
        create_header(course, module_id, 'Actividades')
        create_header(course, module_id, 'Material de clase')

    if is_visible_links:
        prefixes = [('Grabación ', 'http://tu_grabacion_en_zoom.com'),('', zoom_url)]
        for prefix, url in prefixes:
            data = {}
            data['module_item[title]'] = format_title( date.strftime("%d"), date.strftime("%m"), "{:02d}".format(i), prefix=prefix)
            data['module_item[type]'] = 'ExternalUrl'
            data['module_item[position]'] = '1'
            data['module_item[indent]'] = '1'
            data['module_item[external_url]'] = url
            data['module_item[new_tab]'] = 1

            new_item = post_item(course, module_id, data)
first_date = datetime.datetime(2020, 9, dia)
delta = timedelta(days = 7)

def get_course_name(course_details):
    big_name = course_details['name']
    parts = big_name.split("-")
    name = re.sub(r"\([A-Z0-9]{6,}\) $","", parts[0])
    return name.strip()

def check_expression(regex, text):
    x = re.match(regex, text)
    if x != None :
        return True

def check_name(part, name):
    regex = "^(2020-1) [A-Z0-9]{6,} (ES|EN) ("+name+")$"
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
    regex = "^\d\d\:\d\d\ ?-\ ?\d\d\:\d\d$"
    return check_expression(regex, part)

def check_type(part):
    regex = "(Teoría)|(Laboratorio)$"
    return check_expression(regex, part)

def check_url(part):
    regex = "^https://utec.zoom.us/"
    return check_expression(regex, part)

def check_published(part):
    return part

def check_videoconferencia(items, name):
    for item in items:
        #print(item)
        if item['type'] == 'ExternalUrl' and item['title'].startswith('2020'):
            print(item['title'])
            parts =  re.split('; |, ', item['title'])
            print(parts[0],check_name(parts[0].strip(), name))
            print(parts[1],check_section(parts[1].strip()))
            print(parts[2],check_week(parts[2].strip()))
            print(parts[3],check_professor(parts[3].strip()))
            print(parts[4],check_date(parts[4].strip()))
            print(parts[5],check_hour(parts[5].strip()))
            print(parts[6],check_type(parts[6].strip()))
            print(item['external_url'],check_url(item['external_url'].strip()))
            print(item['published'],check_published(item['published']))

i = 0
course_details = canvas.get_course(course)
canvas_course_name = get_course_name(course_details)

for module in  canvas.get_modules(course):
    if module['name'].startswith('Semana '):
        #print(module)
        i += 1
        if i >= first_week and i <= last_week :
            items = canvas.get_items(course, module['id'])
            check_videoconferencia(items, canvas_course_name)
        first_date = first_date + delta

#print(modules)
