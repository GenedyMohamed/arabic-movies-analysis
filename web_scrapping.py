from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import unicodedata as ud
import re

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

def add_to_csv(dict):
    f = open('data.csv', 'a', encoding="utf-8")
    if (isinstance(dict, str)):
        f.write('\n'+dict)
    else:
        f.write('\n')
        for value in dict.values():
            f.write(value+', ')
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
        print("Year: 19"+str(i))
        for j in range(1, 100):
            # time.sleep(1)
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
                            dict = {'year': 19+str(i), 'movie_name': movie_name, 'movie_link': movie_link}
                            dict.update(get_film_details(dict['movie_link']))
                            add_to_csv(dict)

def get_film_details(movie_link):
    raw_html = simple_get("https://www.elcinema.com"+movie_link)
    write_html(raw_html, "page.html")
    html = read_html(raw_html)
    dict = {}
    #"التقييم"# 
    found = False
    for ul in html.select("ul"):
        div_tags = ul.findAll("div", recursive=True)
        for div in div_tags:
            if (div.find("span")):
                print(div.find("span").text)
                found = True
                break
        if (found):
            break
    #"المدة"# 
    found = False
    for ul in html.select("ul"):
        li_tags = ul.findAll("li", recursive=False)
        for li in li_tags:
            if ("دقيقة" in li.text):
                print((li.text).split(" ")[0])
                found = True
                break
        if (found):
            break
    #"التفاصيل"# 
    found = False
    for p in html.select("p"):
        span_tags = p.findAll("span", recursive=False)
        for span in span_tags:
            if (span["class"][0] == "hide"):
                dict['description'] = (p.text).replace('...اقرأ المزيد', '') 
                found = True
                break
        if (found):
            break
    #"تاريخ العرض"#    
    for a in html.select("a"):
        if(a.has_attr('href') and  "release_day" in a['href']):
            print(a.text)
            break
    #"إخراج"#    
    cast_html = read_html(simple_get("https://www.elcinema.com"+movie_link+"cast"))
    
    directors = []
    for li in cast_html.select("li"):
        if("مخرج" in li.text):
            director_li = li.parent.findAll("li", recursive=False)[0]
            director_a = director_li.find("a", recursive=False)
            
            if(director_a is not None):
                directors.append(director_a.text)
    print(directors)
    
    #"تصنيف الفيلم"#    
    genres = []
    for a in html.select("a"):
        if(a.has_attr('href') and "genre" in a['href'] and not("المزيد" in a.text)):
            genres.append(a.text)
    genres = list(set(genres))
    if(len(genres)>0):
        print(genres[0])
        
    #"تمثيل"#    
    actors = []
    num_actors = 0
    for h3 in cast_html.select("h3"):
        if("ﺗﻤﺜﻴﻞ" in h3.text): #and h3.find("span", recursive=False)):
            
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_actors = int(x.group())
            num_actors = number_of_actors
            for li in cast_html.select("li"):
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        actors.append(a.text)
                        number_of_actors -= 1
                if (number_of_actors == 0):
                    break
            print(actors)
             
    #"تأليف"#    
    writers = []
    for h3 in cast_html.select("h3"):
        if("ﺗﺄﻟﻴﻒ" in h3.text): #and h3.find("span", recursive=False)):
            
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_writers = int(x.group())
            for li in cast_html.select("li"):
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        if(num_actors == 0):
                            
                            writers.append(a.text)
                            number_of_writers -= 1
                        else:
                            num_actors -= 1
                if (number_of_writers == 0):
                    break
            print(writers)
            
    musicians = []
    for h3 in cast_html.select("h3"):
        if("ﻣﻮﺳﻴﻘﻰ" in h3.text):
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_musicians = int(x.group())
            lis = h3.parent.parent.findAll("li")
            for li in lis:
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        musicians.append(a.text)
                        number_of_musicians -= 1
                if(number_of_musicians == 0):
                     break
            print("Musicians: ")
            print(musicians)
            break
    
    decor = []
    for h3 in cast_html.select("h3"):
        if("ﺩﻳﻜﻮﺭ" in h3.text):
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_decorators = int(x.group())
            lis = h3.parent.parent.findAll("li")
            for li in lis:
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        decor.append(a.text)
                        number_of_decorators -= 1
                if(number_of_decorators == 0):
                     break
            print("Decor: ")
            print(decor)
            break
    photographers = []
    for h3 in cast_html.select("h3"):
        if("ﺗﺼﻮﻳﺮ" in h3.text):
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_photographers = int(x.group())
            lis = h3.parent.parent.findAll("li")
            for li in lis:
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        photographers.append(a.text)
                        number_of_photographers -= 1
                if(number_of_photographers == 0):
                     break
            print("Photographers: ")
            print(photographers)
            break
    
    montage = []
    for h3 in cast_html.select("h3"):
        if("ﻣﻮﻧﺘﺎﺝ" in h3.text):
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_montage = int(x.group())
            lis = h3.parent.parent.findAll("li")
            for li in lis:
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        montage.append(a.text)
                        number_of_montage -= 1
                if(number_of_montage == 0):
                     break
            print("Montage: ")
            print(montage)
            break
    return dict
