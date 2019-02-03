from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def simple_get(url):
    # Attemps to get the content at 'url' by making an HTTP GET request.
    # If the content-type of response is some kind of HTML/XML, return the text content, otherwise return None.
    try:
        with get(url, stream=True) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    # Returns true if the response seems to be HTML, False otherwise.
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def log_error(e):
    # This function prints log errors
    print(e)

def write_html(raw_html):
    f = open("page.html", "w+", encoding="utf-8")
    html = BeautifulSoup(raw_html, 'html.parser')
    f.write(str(html.encode("utf-8")))
    f.close()

