from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import unicodedata as ud

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

def write_html(raw_html, filename):
    f = open(filename, "w+", encoding="utf-8")
    try:
        html = BeautifulSoup(raw_html, 'html.parser')
    except:
        html = BeautifulSoup("404 Not Found!", 'html.parser')
    f.write(html.__unicode__())
    f.close()

def read_html(raw_html):
    try:
        html = BeautifulSoup(raw_html, 'html.parser')
    except:
        html = BeautifulSoup("404 Not Found!", 'html.parser')
    return html#.__unicode__()

def add_to_csv(year, title, link):
    f = open('data.csv', 'a', encoding="utf-8")
    f.write('\n'+year+', '+title+', '+link)
    f.close()

#Check if word is in Latin alphabet or not.
latin_letters= {}
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))
def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha())

def add_films_to_csv():
    for i in range(77, 80): # get arabic movie names and links from year 1977 to 1979
        print(i)
        for j in range(1, 100):
            raw_html = simple_get("https://www.elcinema.com/index/work/release_year/19{}?page={}".format(i, j))
            print(j)
            if(raw_html is None):
                break
            html = read_html(raw_html)
            for td in html.select("td"):
                a_tags = td.findAll("a", recursive=False)
                for a in a_tags:
                    if(a.find("img") and td.parent.find("td", string="فيلم")):
                        movie = a.parent.findAll("a", recursive=False)[-1]
                        movie_name = movie.text
                        if(not only_roman_chars(movie_name)):
                            movie_link = movie['href']
                            add_to_csv("19"+str(i), movie_name, movie_link)

