import datetime
import canvas
from datetime import timedelta
import json

#####################################################################################################
#                                   Just config your course here                                    #
course               = '5662'   # From Canvas
course_cod           = 'CS4002' # From our curricula at the university
course_name          = 'Proyecto Final de Carrera I'
course_section       = '1' #CURSO-SECCIÓN
course_professor     = 'Yamilet Serrano'
course_type          = 'Teoría' #"TIPO [Teoría|Labotorio]:")
course_starts        = '19:00'  #input("HORA INICIO: HH:mm ")
course_ends          = '20:00'  #input("HORA FIN: HH:mm ")
dia                  = 3        #primer día de clases en Abril.
zoom_url             = 'https://utec.zoom.us/j/97175965748'       #input("LINK ZOOM:")
first_week           = 6        # from this week
last_week            = 6        # until this week

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

i = 0
for module in  canvas.get_modules(course):
    if module['name'].startswith('Semana '):
        i += 1
        if i >= first_week and i <= last_week :
            print("Configuring", module['name'])
            configure_week(module['id'], first_date)
        first_date = first_date + delta
print('It seams we finished ... please REFRESH your browser to see to new configuration !')
print('This small program was created by Jesus Bellido <jbellido@utec.edu.pe>')

#print(modules)
