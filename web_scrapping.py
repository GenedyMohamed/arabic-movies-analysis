from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import unicodedata as ud
import re
import csv

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
    f = open('data.csv', 'a', newline='', encoding="utf-8")
    writer = csv.writer(f)
    arr = []
    for value in dict.values():
        arr.append(value)
    writer.writerow(arr)
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

def get_avg_duration(year):
    sum = 0
    count = 0
    for j in range(1, 100):
        raw_html = simple_get("https://www.elcinema.com/index/work/release_year/{}?page={}".format(year, j))
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
                        dict = {'السنه': str(year), 'اسم الفيلم': movie_name, 'movie_link': movie_link}
                        dict.update(get_film_details(dict['movie_link']))
                        if (not dict['مدة الفيلم'] == ''):
                            sum += int(dict['مدة الفيلم'])
                            count += 1
    return sum/count

def add_films_to_csv():
    for i in range(40, 80): # get arabic movie names and links from year 1977 to 1979
        print("Year: 19"+str(i))
        avg = "{:.1f}".format(float(get_avg_duration(int('19'+str(i)))))
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
                            dict = {'السنه': str(19)+str(i), 'اسم الفيلم': movie_name, 'movie_link': movie_link}
                            dict.update(get_film_details(dict['movie_link']))
                            if (dict['مدة الفيلم'] == ''):
                                dict['مدة الفيلم'] = str(avg)
                            dict2 = {'اسم الفيلم': dict['اسم الفيلم'], 'تاريخ العرض': dict['تاريخ العرض']+' '+str(19)+str(i), 'تصنيف الفيلم': dict['تصنيف الفيلم'], 'مدة الفيلم': dict['مدة الفيلم'], 'ملخص': dict['ملخص'], 'تأليف': dict['تأليف'], 'تمثيل': dict['تمثيل'], 'إنتاج': dict['إنتاج'], 'تصوير': dict['تصوير'], 'مونتاج': dict['مونتاج'], 'ديكور': dict['ديكور'], 'ملابس': dict['ملابس'], 'موسيقى': dict['موسيقى'], 'إخراج': dict['إخراج'], 'إنتاج': dict['إنتاج'], 'توزيع': dict['توزيع']}
                            add_to_csv(dict2)

def get_film_details(movie_link):
    raw_html = simple_get("https://www.elcinema.com"+movie_link)
    html = read_html(raw_html)
    dict = {}
    #"التقييم"# 
    found = False
    dict['التقييم'] = ''
    for ul in html.select("ul"):
        div_tags = ul.findAll("div", recursive=True)
        for div in div_tags:
            if (div.find("span")):
                dict['التقييم'] = div.find("span").text
                found = True
                break
        if (found):
            break
    #"مدة الفيلم"# 
    found = False
    dict['مدة الفيلم'] = ''
    for ul in html.select("ul"):
        li_tags = ul.findAll("li", recursive=False)
        for li in li_tags:
            if ("دقيقة" in li.text):
                dict['مدة الفيلم'] = (li.text).split(" ")[0]
                found = True
                break
        if (found):
            break
    #"ملخص"# 
    found = False
    dict['ملخص'] = ''
    for p in html.select("p"):
        span_tags = p.findAll("span", recursive=False)
        for span in span_tags:
            if (span["class"][0] == "hide"):
                dict['ملخص'] = ((p.text).replace('...اقرأ المزيد', '')).replace('\n', ' ')
                found = True
                break
        if (found):
            break
    #"تاريخ العرض"#  
    dict['تاريخ العرض'] = ''  
    for a in html.select("a"):
        if(a.has_attr('href') and  "release_day" in a['href']):
            dict['تاريخ العرض'] = a.text
            break
    #"إخراج"#    
    cast_html = read_html(simple_get("https://www.elcinema.com"+movie_link+"cast"))
    
    directors = []
    dict['إخراج'] = ''
    for li in cast_html.select("li"):
        if("مخرج" in li.text):
            director_li = li.parent.findAll("li", recursive=False)[0]
            director_a = director_li.find("a", recursive=False)
            
            if(director_a is not None):
                directors.append(director_a.text)
    dict['إخراج'] = directors
    
    #"تصنيف الفيلم"#    
    genres = []
    dict['تصنيف الفيلم'] = ''
    for a in html.select("a"):
        if(a.has_attr('href') and "genre" in a['href'] and not("المزيد" in a.text)):
            genres.append(a.text)
    genres = list(set(genres))
    if(len(genres)>0):
        dict['تصنيف الفيلم'] = genres[0]
        
    #"تمثيل"#    
    actors = []
    num_actors = 0
    dict['تمثيل'] = ''
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
            dict['تمثيل'] = actors
             
    #"تأليف"#    
    writers = []
    dict['تأليف'] = ''
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
            dict['تأليف'] = writers
            
    musicians = []
    dict['موسيقى'] = ''
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
            dict['موسيقى'] = musicians
            break
    
    decor = []
    dict['ديكور'] = ''
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
            dict['ديكور'] = decor
            break
    photographers = []
    dict['تصوير'] = ''
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
            dict['تصوير'] = photographers
            break
    
    montage = []
    dict['مونتاج'] = ''
    for h3 in cast_html.select("h3"):
        if("ﻣﻮﻧﺘﺎﺝ" in h3.text or "مونتاج" in h3.text):
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
            dict['مونتاج'] = montage
            break
        
    production =[]
    dict['إنتاج'] = ''
    for h3 in cast_html.select("h3"):
        if("اﻧﺘﺎﺝ" in h3.text or "إنتاج" in h3.text):
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_producers = int(x.group())
            lis = h3.parent.parent.findAll("li")
            for li in lis:
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        production.append(a.text)
                        number_of_producers -= 1
                if(number_of_producers == 0):
                     break
            dict['إنتاج'] = production
            break
    
    publishing =[]
    dict['توزيع'] = ''
    for h3 in cast_html.select("h3"):
        if("ﺗﻮﺯﻳﻊ" in h3.text or "توزيع" in h3.text):
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_publishers = int(x.group())
            lis = h3.parent.parent.findAll("li")
            for li in lis:
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        publishing.append(a.text)
                        number_of_publishers -= 1
                if(number_of_publishers == 0):
                     break
            dict['توزيع'] = publishing
            break
        
    clothes =[]
    dict['ملابس'] = ''
    for h3 in cast_html.select("h3"):
        if("ﻣﻼﺑﺲ" in h3.text or "ملابس" in h3.text):
            span = h3.find("span", recursive=False)
            x = re.search(r'\d+', span.text)
            number_of_clothes = int(x.group())
            lis = h3.parent.parent.findAll("li")
            for li in lis:
                if(li.find("a")):
                    a = li.find("a")
                    if(a.has_attr("href") and "person" in a['href']):
                        clothes.append(a.text)
                        number_of_clothes -= 1
                if(number_of_clothes == 0):
                     break
            dict['ملابس'] = clothes
            break
    
    return dict
