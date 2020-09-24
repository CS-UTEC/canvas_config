import requests

url_course  = '<path>/<course>'
url_modules = '<path>/<course>/modules?per_page=40'
url_items   = '<path>/<course>/modules/<module>/items?per_page=40'
url_item    = "<path>/<course>/modules/<module>/items/<item>"
path        = 'https://utec.instructure.com/api/v1/courses'
access_token         = ""

def headers():
    token = 'Bearer '+access_token
    return {'Authorization': token}

def get(url):
    url = url.replace('<path>', path)
    r = requests.get(url, headers = headers())
    if r.status_code >= 400:
        raise Exception("Unauthorized, Verify course and access_token")
    return r.json()

def post(url, data):
    url = url.replace('<path>', path)
    r = requests.post(url, headers = headers(), data = data)
    if r.status_code >= 400:
        raise Exception("Unauthorized, Verify course and access_token")
    return r.json()

def put(url, data):
    url = url.replace('<path>', path)
    try:
        r = requests.put(url, headers = headers(), data = data)
        print(r.json())
        r.raise_for_status()
    except Exception as e:
        print(e)
    #if r.status_code >= 400:
    #    raise Exception("Unauthorized, Verify course and access_token")
    return r.json()

def get_course(course):
    url = url_course
    url = url.replace('<course>', course)
    return get(url)

def get_modules(course):
    url = url_modules
    url = url.replace('<course>', course)
    return get(url)

def get_items(course, module):
    url = url_items
    url = url.replace('<course>', course)
    url = url.replace('<module>', str(module))
    return get(url)

def post_item(course, module, item):
    url = url_items
    url = url.replace('<course>', course)
    url = url.replace('<module>', str(module))
    return  post(url, item)

def update_item(course, module, item, data):
    url = url_item
    url = url.replace('<course>', course)
    url = url.replace('<module>', str(module))
    url = url.replace('<item>', str(item))
    return  put(url, data)

def format_title( dia, mes, semana, prefix ='' ):
    format = '<prefix>2020-1 <course_cod> ES <course_name>, <course_section>, Semana<course_semana>, <course_professor>, <course_mes>/<course_dia>, <course_starts> - <course_ends> <course_type>'
    format = format.replace('<course_cod>', course_cod)
    format = format.replace('<course_name>', course_name)
    format = format.replace('<course_section>', course_section)
    format = format.replace('<course_mes>', mes)
    format = format.replace('<course_dia>', dia)
    format = format.replace('<course_starts>', course_starts)
    format = format.replace('<course_ends>', course_ends)
    format = format.replace('<course_semana>', semana)
    format = format.replace('<course_professor>', course_professor)
    format = format.replace('<course_type>', course_type)
    format = format.replace('<prefix>', prefix)
    return format

def create_header(course, module, titulo):
    data = {}
    data['module_item[title]'] = titulo
    data['module_item[type]'] = 'SubHeader'
    data['module_item[position]'] = '1'
    data['module_item[indent]'] = '0'
    new_item = post_item(course, module, data)
