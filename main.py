from web_scrapping import simple_get, write_html

raw_html = simple_get('https://www.elcinema.com/')
write_html(raw_html)