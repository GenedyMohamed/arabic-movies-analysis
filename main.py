from web_scrapping import simple_get, write_html, read_html, add_to_csv
import unicodedata as ud

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


for i in range(77, 80): # get arabic movie names and links from year 1977 to 1979
    print(i)
    for j in range(1, 100):
        raw_html = simple_get("https://www.elcinema.com/index/work/release_year/19{}?page={}".format(i, j))
        print(j)
        if(raw_html is None):
            break
        #write_html(raw_html, 'page.html')
        
        html = read_html(raw_html)
        flag = False
        for td in html.select("td"):
            a_tags = td.findAll("a", recursive=False)
            for a in a_tags:
                if(a.find("img") and td.parent.find("td", string="فيلم")):
                    movie = a.parent.findAll("a", recursive=False)[-1]
                    movie_name = movie.text
                    if(not only_roman_chars(movie_name)):
                        movie_link = movie['href']
                        print(movie_name)
                        print(movie_link)
                        #add_to_csv('1979', movie_name, movie_link)
            
            




